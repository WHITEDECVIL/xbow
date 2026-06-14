"""
Configuration Management Module
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import os


CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
CONFIG_DIR.mkdir(exist_ok=True)


@dataclass
class ScanConfig:
    """Configuration for scanning operations"""
    timeout: int = 30
    retries: int = 3
    threads: int = 4
    verbose: bool = False
    log_level: str = "INFO"
    output_dir: str = "results"
    auto_exploit: bool = False


@dataclass
class AIConfig:
    """AI/ML Engine Configuration"""
    model_path: str = "models/vulnerability_classifier.pkl"
    enable_ml: bool = True
    confidence_threshold: float = 0.7
    enable_predictions: bool = True
    enable_agent: bool = False
    agent_provider: str = "mock"
    agent_model: str = "gpt-4o-mini"
    agent_endpoint: str = "https://api.openai.com/v1/chat/completions"
    agent_api_key_env: str = "OPENAI_API_KEY"
    agent_settings: Dict[str, Any] = None


@dataclass
class NetworkConfig:
    """Network scanning configuration"""
    enable_ping_sweep: bool = True
    enable_port_scan: bool = True
    port_range: str = "1-65535"
    enable_service_detection: bool = True
    enable_os_detection: bool = True


@dataclass
class WebConfig:
    """Web application scanning configuration"""
    follow_redirects: bool = True
    verify_ssl: bool = False
    custom_headers: Dict[str, str] = None
    enable_js_analysis: bool = True
    crawl_depth: int = 3


class ConfigManager:
    """Manages XBOW configuration"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or CONFIG_DIR / "xbow.json"
        self.scan_config = ScanConfig()
        self.ai_config = AIConfig()
        self.network_config = NetworkConfig()
        self.web_config = WebConfig()
        self._load_config()
    
    def _update_config(self, config_obj: Any, values: Dict[str, Any]):
        for key, value in values.items():
            if hasattr(config_obj, key):
                setattr(config_obj, key, value)

    def _load_config(self):
        """Load configuration from file if exists"""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    
                if 'scan' in data:
                    self._update_config(self.scan_config, data['scan'])
                if 'ai' in data:
                    self._update_config(self.ai_config, data['ai'])
                if 'network' in data:
                    self._update_config(self.network_config, data['network'])
                if 'web' in data:
                    self._update_config(self.web_config, data['web'])
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        config_data = {
            'scan': asdict(self.scan_config),
            'ai': asdict(self.ai_config),
            'network': asdict(self.network_config),
            'web': asdict(self.web_config),
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def update_scan_config(self, **kwargs):
        """Update scan configuration"""
        for key, value in kwargs.items():
            if hasattr(self.scan_config, key):
                setattr(self.scan_config, key, value)
    
    def get_output_dir(self) -> Path:
        """Get output directory, creating if needed"""
        output_dir = Path(self.scan_config.output_dir)
        output_dir.mkdir(exist_ok=True)
        return output_dir


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def init_config(config_file: Optional[str] = None) -> ConfigManager:
    """Initialize configuration manager"""
    global _config_manager
    _config_manager = ConfigManager(config_file)
    return _config_manager
