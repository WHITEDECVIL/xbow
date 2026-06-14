"""
Advanced Injection Detection Module
Implements timing-based, error-based, and DOM-based injection detection
"""

import time
import re
from typing import Dict, Optional, List
from src.utils.logger import logger, color_logger


class AdvancedInjectionDetector:
    """Advanced SQL injection and XSS detection techniques"""
    
    def __init__(self):
        # SQL error patterns (database-agnostic)
        self.sql_error_patterns = [
            r"SQL syntax",
            r"mysql_fetch_array",
            r"Warning: mysql_",
            r"mysql_num_rows",
            r"OracleException",
            r"PostgreSQL",
            r"MSSQL",
            r"Syntax error",
            r"SQL command not properly ended",
            r"SQLServer.GetType",
            r"Invalid column name",
            r"Unclosed quotation mark",
        ]
        
        # XSS detection patterns
        self.xss_patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"onclick=",
            r"<iframe",
            r"<embed",
            r"<object",
            r"<img[^>]*src=",
        ]
        
        # DOM-XSS sinks
        self.dom_sinks = [
            'innerHTML',
            'outerHTML',
            'document.write',
            'eval',
            'setTimeout',
            'setInterval',
            'Function',
        ]
    
    def detect_error_based_sqli(self, response_text: str, payload: str) -> Dict:
        """Detect SQL injection via error messages"""
        findings = {
            'vulnerable': False,
            'confidence': 0.0,
            'error_patterns_found': [],
            'payload': payload,
        }
        
        for pattern in self.sql_error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                findings['error_patterns_found'].append(pattern)
                findings['vulnerable'] = True
                findings['confidence'] = min(1.0, findings['confidence'] + 0.2)
        
        # Check for UNION-based indicators
        if re.search(r'column.*count|order by', response_text, re.IGNORECASE):
            findings['confidence'] = min(1.0, findings['confidence'] + 0.1)
        
        return findings
    
    def detect_timing_based_sqli(self, url: str, session, timeout: int = 10) -> Dict:
        """Detect SQL injection via response time analysis (blind SQLi)"""
        findings = {
            'vulnerable': False,
            'confidence': 0.0,
            'timing_delta': 0.0,
            'technique': 'timing-based',
        }
        
        try:
            # Baseline request
            start = time.time()
            session.get(url, timeout=timeout)
            baseline = time.time() - start
            
            # Sleep-based payload (SLEEP if MySQL, WAITFOR if MSSQL)
            sleep_payloads = [
                "SLEEP(5)",
                "WAITFOR DELAY '00:00:05'",
            ]
            
            for payload_str in sleep_payloads:
                test_url = f"{url}&sleep={payload_str}"
                try:
                    start = time.time()
                    session.get(test_url, timeout=timeout + 10)
                    delayed = time.time() - start
                    delta = delayed - baseline
                    
                    # If response delayed by ~5 seconds, likely vulnerable
                    if delta > 4.0:
                        findings['vulnerable'] = True
                        findings['confidence'] = 0.95
                        findings['timing_delta'] = delta
                        break
                except:
                    pass
        
        except Exception as e:
            logger.debug(f"Timing-based SQLi detection error: {e}")
        
        return findings
    
    def detect_xss_in_response(self, payload: str, response_text: str) -> Dict:
        """Detect reflected XSS with context analysis"""
        findings = {
            'reflected': False,
            'contexts': [],
            'confidence': 0.0,
            'payload': payload,
        }
        
        if payload not in response_text:
            return findings
        
        findings['reflected'] = True
        
        # Analyze context (where payload appears)
        contexts = {
            'in_html': r'<[^>]*' + re.escape(payload) + r'[^>]*>',
            'in_attribute': r'(src|href|onclick|onerror|style)="[^"]*' + re.escape(payload),
            'in_script': r'<script[^>]*>.*' + re.escape(payload),
            'unescaped': True,  # Default to unescaped
        }
        
        for context, pattern in contexts.items():
            if context == 'unescaped':
                # Check if payload is HTML/JS escaped
                if any(esc in response_text for esc in ['&lt;', '&#', '%3C', '&#x']):
                    findings['contexts'].append('escaped')
                    findings['confidence'] -= 0.2
            elif re.search(pattern, response_text):
                findings['contexts'].append(context)
                findings['confidence'] = min(1.0, findings['confidence'] + 0.25)
        
        if not findings['contexts']:
            findings['contexts'] = ['text_node']
            findings['confidence'] = 0.6
        
        return findings
    
    def detect_dom_xss_vulnerability(self, html_content: str) -> Dict:
        """Detect DOM-based XSS vulnerabilities (JavaScript analysis)"""
        findings = {
            'vulnerable': False,
            'sinks_found': [],
            'sources_found': [],
            'confidence': 0.0,
        }
        
        # Find dangerous sinks
        for sink in self.dom_sinks:
            if sink in html_content:
                findings['sinks_found'].append(sink)
        
        # Find sources (user-controllable input)
        sources = [
            'location.hash',
            'location.search',
            'document.cookie',
            'window.name',
            'document.referrer',
        ]
        
        for source in sources:
            if source in html_content:
                findings['sources_found'].append(source)
        
        # Vulnerable if both sink and source found without sanitization
        if findings['sinks_found'] and findings['sources_found']:
            findings['vulnerable'] = True
            findings['confidence'] = 0.8
        
        return findings
    
    def detect_command_injection(self, payload: str, response_text: str) -> Dict:
        """Detect OS command injection"""
        findings = {
            'vulnerable': False,
            'indicators': [],
            'confidence': 0.0,
        }
        
        # Command output indicators
        indicators = [
            r'uid=\d+',  # Linux id output
            r'C:\\',  # Windows paths
            r'bin/bash',
            r'total \d+',  # ls -la output
            r'drwxr',  # Unix permissions
        ]
        
        for indicator in indicators:
            if re.search(indicator, response_text):
                findings['indicators'].append(indicator)
                findings['vulnerable'] = True
                findings['confidence'] = min(1.0, findings['confidence'] + 0.25)
        
        return findings
    
    def detect_ldap_injection(self, payload: str, response_text: str) -> Dict:
        """Detect LDAP injection"""
        findings = {
            'vulnerable': False,
            'confidence': 0.0,
        }
        
        # LDAP error patterns
        ldap_errors = [
            r'LDAP error',
            r'LDAP syntax',
            r'ldap_bind',
            r'Invalid DN',
        ]
        
        for error in ldap_errors:
            if re.search(error, response_text, re.IGNORECASE):
                findings['vulnerable'] = True
                findings['confidence'] = 0.8
                break
        
        return findings
