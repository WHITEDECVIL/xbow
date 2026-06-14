"""
AI Agent API integration module.

This module provides an extensible AI agent interface for live automated pentesting.
Agents can be configured via config/ai_agents.json and used to recommend next actions
for auto mode.
"""

import json
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from src.utils.logger import color_logger, logger

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
AGENT_CONFIG_FILE = CONFIG_DIR / "ai_agents.json"

DEFAULT_AGENT_CONFIG = {
    "enabled": False,
    "default_agent": "mock",
    "providers": {
        "mock": {
            "name": "MockAgent",
            "enabled": True,
            "description": "Fallback local decision agent when no API key is configured."
        },
        "openai": {
            "name": "OpenAI",
            "enabled": False,
            "model": "gpt-4o-mini",
            "endpoint": "https://api.openai.com/v1/chat/completions",
            "api_key_env": "OPENAI_API_KEY",
            "description": "OpenAI chat model provider for action orchestration."
        }
    }
}


class AIBaseAgent(ABC):
    """Generic AI agent interface for XBOW."""

    def __init__(self, provider_config: Dict[str, Any]):
        self.provider_config = provider_config
        self.name = provider_config.get("name", "UnknownAgent")
        self.enabled = provider_config.get("enabled", False)

    @abstractmethod
    def recommend_next_action(self, target: str, session_vulns: List[Dict[str, Any]], analyzer) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def _normalize_action(self, action: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not action or not isinstance(action, dict):
            return None
        action_type = action.get("type")
        if action_type not in ["scan", "exploit", "nmap", "sqlmap", "wait", "stop"]:
            return None
        return action


class MockAIAgent(AIBaseAgent):
    """Fallback local decision agent when no external provider is available."""

    def recommend_next_action(self, target: str, session_vulns: List[Dict[str, Any]], analyzer) -> Optional[Dict[str, Any]]:
        if not session_vulns:
            return {"type": "scan", "scan_type": "web"}

        high_severity = [v for v in session_vulns if v.get("severity") in ["HIGH", "CRITICAL"]]
        unattempted_high = [v for v in high_severity if v.get("exploit_attempts", 0) == 0]
        sql_vulns = [v for v in session_vulns if "sql" in v.get("type", "").lower()]
        scanned_nmap = any("nmap" in str(v.get("scan_result", "")) for v in session_vulns)

        if unattempted_high:
            vuln = unattempted_high[0]
            return {"type": "exploit", "vuln_id": vuln.get("id")}
        if sql_vulns and not any("sqlmap" in str(v.get("exploitation_result", "")) for v in session_vulns):
            vuln = sql_vulns[0]
            return {"type": "sqlmap", "url": vuln.get("url", target), "options": "--batch --level=3 --risk=2"}
        if not scanned_nmap:
            return {"type": "nmap", "options": "-sV -p 1-1000"}
        if len(session_vulns) < 10:
            return {"type": "scan", "scan_type": "web"}
        return {"type": "wait", "seconds": 30}


class OpenAIChatAgent(AIBaseAgent):
    """OpenAI-based AI orchestration agent."""

    def recommend_next_action(self, target: str, session_vulns: List[Dict[str, Any]], analyzer) -> Optional[Dict[str, Any]]:
        api_key = os.getenv(self.provider_config.get("api_key_env", "OPENAI_API_KEY"))
        if not api_key:
            color_logger.warning("OpenAI API key not configured. Falling back to mock agent.", "AI_AGENT")
            return None

        prompt = self._build_prompt(target, session_vulns)
        response = self._call_openai(prompt, api_key)
        action = self._parse_response(response)
        if action:
            return self._normalize_action(action)
        return None

    def _build_prompt(self, target: str, session_vulns: List[Dict[str, Any]]) -> str:
        vuln_summary = []
        for vuln in session_vulns:
            vuln_summary.append({
                "id": vuln.get("id"),
                "name": vuln.get("name"),
                "type": vuln.get("type"),
                "severity": vuln.get("severity"),
                "url": vuln.get("url"),
                "confidence": vuln.get("confidence", 0.0),
            })

        prompt = (
            "You are an AI pentest orchestration agent for XBOW. "
            "Given the target and discovered vulnerabilities, decide the next safe action. "
            "Return only a single JSON object with keys: type, scan_type, vuln_id, url, options, seconds. "
            "Allowed types are: scan, exploit, nmap, sqlmap, wait, stop. "
            "Do not include any markdown formatting. "
            f"Target: {target}\n"
            f"Vulnerabilities: {json.dumps(vuln_summary)}\n"
            "Choose the next highest-value action to progress the automated pentest." 
        )
        return prompt

    def _call_openai(self, prompt: str, api_key: str) -> Optional[Dict[str, Any]]:
        try:

            endpoint = self.provider_config.get("endpoint", "https://api.openai.com/v1/chat/completions")
            if not endpoint:
                logger.error("OpenAI endpoint not configured")
                return None
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            payload = {
                "model": self.provider_config.get("model", "gpt-4o-mini"),
                "messages": [
                    {"role": "system", "content": "You are a penetration testing orchestration assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.25,
                "max_tokens": 250,
            }
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            return None

    def _parse_response(self, response: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not response:
            return None

        text = ""
        choices = response.get("choices") or []
        if choices:
            message = choices[0].get("message", {})
            text = message.get("content", "")

        if not text:
            return None

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON action from AI response: {e}")
            return None


class AIProviderManager:
    """Loads AI agent provider configurations and creates agent instances."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = Path(config_path or AGENT_CONFIG_FILE)
        self.config = self._load_config()
        self.providers = self.config.get("providers", DEFAULT_AGENT_CONFIG["providers"])
        self.default_agent = self.config.get("default_agent", "mock")
        self.enabled = self.config.get("enabled", False)

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                return {**DEFAULT_AGENT_CONFIG, **data}
            except Exception as e:
                logger.error(f"Failed to load AI agent configuration: {e}")
        return DEFAULT_AGENT_CONFIG

    def get_provider_config(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        provider_name = provider_name or self.default_agent
        return self.providers.get(provider_name, self.providers.get("mock", {}))

    def create_agent(self, provider_name: Optional[str] = None) -> AIBaseAgent:
        provider = self.get_provider_config(provider_name)
        if provider.get("name", "").lower() == "openai" and provider.get("enabled", False):
            return OpenAIChatAgent(provider)
        return MockAIAgent(provider)
