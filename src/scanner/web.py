"""
Web Application Scanner Module
"""

import requests
import re
import warnings
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json

from src.utils.logger import logger, color_logger
from src.utils.helpers import RiskLevel
from src.scanner.advanced_detection import AdvancedInjectionDetector
from src.threat_intelligence import ThreatIntelligence
from src.accuracy_metrics import RealTimeAccuracyValidator

# Suppress SSL warnings for penetration testing
warnings.filterwarnings('ignore', message='.*Unverified HTTPS request.*')


@dataclass
class Vulnerability:
    """Found vulnerability"""
    name: str
    type: str
    url: str
    parameter: Optional[str] = None
    payload: Optional[str] = None
    severity: str = RiskLevel.MEDIUM
    description: str = ""
    remediation: str = ""
    evidence: str = ""
    # New fields for professional reporting
    cwe: Optional[str] = None
    owasp: Optional[str] = None
    detection_method: Optional[str] = None
    confidence: float = 0.0
    poc: Optional[str] = None
    # PoC execution results
    poc_response: Optional[str] = None
    poc_response_status: Optional[int] = None
    # Enhanced payload and exploitation details
    payload_type: Optional[str] = None
    exploitation_method: Optional[str] = None
    how_exploit_works: Optional[str] = None


@dataclass
class WebResource:
    """Web resource information"""
    url: str
    status_code: int
    headers: Dict = field(default_factory=dict)
    body: Optional[str] = None
    size: int = 0


class WebScanner:
    """Advanced web application scanner"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = False, auto_exploit: bool = False):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.auto_exploit = auto_exploit
        self.session = requests.Session()
        self.vulnerabilities = []
        
        # Advanced detection modules
        self.injection_detector = AdvancedInjectionDetector()
        self.threat_intel = ThreatIntelligence()
        self.accuracy_validator = RealTimeAccuracyValidator()
        
        # Common injection payloads
        self.injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users--",
            "<script>alert('XSS')</script>",
            "${7*7}",
            "#{7*7}",
            "{{7*7}}",
        ]
        
        # Common default paths to test
        self.default_paths = [
            "/admin", "/login", "/api", "/config", "/backup",
            ".git", ".env", ".htaccess", "web.config",
            "/wp-admin", "/wp-login.php",
            "/phpmyadmin", "/administrator",
        ]
    
    def scan_url(self, url: str, crawl: bool = True, depth: int = 2) -> List[Vulnerability]:
        """Scan web application"""
        color_logger.info(f"Starting web scan on {url}", "WEB")
        
        self.vulnerabilities = []
        visited = set()
        
        # Basic scans
        self._scan_headers(url)
        self._scan_common_paths(url)
        self._scan_injection_points(url)
        
        if crawl:
            self._crawl_site(url, depth, visited)
        
        return self.vulnerabilities
    
    def _scan_headers(self, url: str):
        """Scan security headers"""
        try:
            resp = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            
            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Strict-Transport-Security',
                'Content-Security-Policy',
                'X-XSS-Protection',
            ]
            
            missing_headers = []
            for header in security_headers:
                if header not in resp.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                vuln = Vulnerability(
                    name="Missing Security Headers",
                    type="Security Misconfiguration",
                    url=url,
                    severity=RiskLevel.MEDIUM,
                    description=f"Missing headers: {', '.join(missing_headers)}",
                    remediation="Configure security headers on web server",
                    payload_type="Security Header Analysis",
                    exploitation_method="HTTP Header Inspection",
                    how_exploit_works=f"Security headers are missing from HTTP responses, leaving the application vulnerable to clickjacking (X-Frame-Options), MIME sniffing attacks (X-Content-Type-Options), and other client-side attacks.",
                )
                self.vulnerabilities.append(vuln)
                color_logger.warning(f"Missing headers: {', '.join(missing_headers)}", "HEADERS")
            
            # Check for server information disclosure
            if 'Server' in resp.headers:
                vuln = Vulnerability(
                    name="Server Information Disclosure",
                    type="Information Disclosure",
                    url=url,
                    severity=RiskLevel.LOW,
                    description=f"Server header exposed: {resp.headers['Server']}",
                    remediation="Remove or obfuscate Server header",
                    evidence=resp.headers['Server'],
                    payload_type="HTTP Header Fingerprinting",
                    exploitation_method="Passive header analysis",
                    how_exploit_works=f"The Server header reveals the web server software and version ({resp.headers['Server']}), which can be used by attackers to identify known vulnerabilities and tailor their attacks.",
                )
                self.vulnerabilities.append(vuln)
                color_logger.info(f"Server: {resp.headers['Server']}", "HEADERS")

            # Check for insecure cookie flags (Set-Cookie without Secure/HttpOnly)
            set_cookie = resp.headers.get('Set-Cookie')
            if set_cookie and ('Secure' not in set_cookie or 'HttpOnly' not in set_cookie):
                vuln = Vulnerability(
                    name="Insecure Cookie Configuration",
                    type="Security Misconfiguration",
                    url=url,
                    severity=RiskLevel.MEDIUM,
                    description="Cookies missing Secure and/or HttpOnly flags",
                    remediation="Set Secure and HttpOnly flags on cookies",
                    evidence=set_cookie,
                    cwe='CWE-614',
                    owasp='A05:2021-Security Misconfiguration',
                    detection_method='header_inspection',
                    confidence=0.7,
                )
                self.vulnerabilities.append(vuln)
                color_logger.warning(f"Insecure cookie flags: {set_cookie}", "HEADERS")
        
        except Exception as e:
            logger.error(f"Error scanning headers: {e}")
    
    def _scan_common_paths(self, base_url: str):
        """Scan for common sensitive paths"""
        color_logger.info("Scanning for common sensitive paths", "PATHS")
        
        for path in self.default_paths:
            url = urljoin(base_url, path)
            try:
                resp = self.session.get(
                    url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                if resp.status_code < 400:
                    vuln = Vulnerability(
                        name=f"Sensitive Path Accessible: {path}",
                        type="Sensitive Information Exposure",
                        url=url,
                        severity=RiskLevel.MEDIUM if path.startswith('/.') else RiskLevel.HIGH,
                        description=f"Path {path} is accessible (Status: {resp.status_code})",
                        remediation=f"Restrict access to {path}",
                        payload_type="Path Traversal",
                        exploitation_method="Direct URL access",
                        how_exploit_works=f"The sensitive path {path} is directly accessible via HTTP GET request, potentially exposing administrative interfaces, configuration files, or backup data.",
                    )
                    self.vulnerabilities.append(vuln)
                    color_logger.warning(f"Found: {url} [{resp.status_code}]", "PATH")
            except Exception as e:
                logger.debug(f"Error checking path {path}: {e}")
    
    def _scan_injection_points(self, url: str):
        """Scan for SQL injection and XSS vulnerabilities"""
        color_logger.info("Scanning for injection vulnerabilities", "INJECTION")
        
        parsed = urlparse(url)
        
        # Add test parameters if not present
        test_url = url if '?' in url else f"{url}?id=1"
        
        for payload in self.injection_payloads[:3]:
            try:
                # Test as parameter
                test_payload = f"{test_url}&test={payload}"
                resp = self.session.get(test_payload, timeout=self.timeout, verify=self.verify_ssl)
                
                # Advanced detection: check for reflection + errors + context
                detection_results = {
                    'reflected': payload in resp.text,
                    'error_based': self.injection_detector.detect_error_based_sqli(resp.text, payload),
                    'xss_context': self.injection_detector.detect_xss_in_response(payload, resp.text),
                    'command_injection': self.injection_detector.detect_command_injection(payload, resp.text),
                }
                
                # Determine vulnerability type and confidence
                vuln_type = None
                cwe = None
                owasp = None
                confidence = 0.5
                payload_type = None
                exploitation_method = None
                how_exploit_works = None
                
                if "<script>" in payload:
                    # XSS detection
                    vuln_type = "Cross-Site Scripting (XSS)"
                    cwe = 'CWE-79'
                    owasp = 'A03:2021-Injection'
                    payload_type = "Reflected XSS Payload"
                    exploitation_method = "Client-side JavaScript injection"
                    how_exploit_works = "Malicious JavaScript code is injected into the page and executed in the victim's browser, potentially stealing cookies, session tokens, or performing actions on behalf of the user."
                    
                    if detection_results['reflected']:
                        confidence = 0.85
                    if detection_results['xss_context']['reflected']:
                        confidence = min(1.0, confidence + (detection_results['xss_context']['confidence'] - 0.6))
                elif "' OR '1'='1" in payload:
                    # SQL Injection - Boolean-based
                    vuln_type = "SQL Injection"
                    cwe = 'CWE-89'
                    owasp = 'A03:2021-Injection'
                    payload_type = "Boolean-based SQL Injection Payload"
                    exploitation_method = "SQL query manipulation via boolean logic"
                    how_exploit_works = "The payload modifies the SQL query logic to always return true ('1'='1'), potentially bypassing authentication or exposing sensitive data by manipulating WHERE clauses."
                    
                    if detection_results['reflected']:
                        confidence = 0.75
                    if detection_results['error_based']['vulnerable']:
                        confidence = min(1.0, confidence + (detection_results['error_based']['confidence'] - 0.5))
                elif "'; DROP TABLE" in payload:
                    # SQL Injection - Tautology + DROP
                    vuln_type = "SQL Injection"
                    cwe = 'CWE-89'
                    owasp = 'A03:2021-Injection'
                    payload_type = "Tautology-based SQL Injection with Data Manipulation"
                    exploitation_method = "SQL statement termination and injection"
                    how_exploit_works = "The payload terminates the current SQL statement with a semicolon and injects a malicious DROP TABLE command, potentially destroying database tables if the application has sufficient privileges."
                    
                    if detection_results['reflected']:
                        confidence = 0.75
                    if detection_results['error_based']['vulnerable']:
                        confidence = min(1.0, confidence + (detection_results['error_based']['confidence'] - 0.5))
                
                if detection_results['command_injection']['vulnerable']:
                    vuln_type = "OS Command Injection"
                    cwe = 'CWE-78'
                    payload_type = "OS Command Injection Payload"
                    exploitation_method = "Shell command execution via system calls"
                    how_exploit_works = "The payload is executed as a system command on the server, allowing arbitrary command execution with the privileges of the web application process."
                    confidence = detection_results['command_injection']['confidence']
                
                # Only create vulnerability if confidence high enough
                if confidence >= 0.5 or detection_results['reflected']:
                    
                    vuln = Vulnerability(
                        name=f"Potential {vuln_type}",
                        type=vuln_type,
                        url=test_payload,
                        parameter="test",
                        payload=payload,
                        severity=RiskLevel.HIGH,
                        description=f"Advanced analysis detected {vuln_type}: reflection={detection_results['reflected']}, error_patterns={bool(detection_results['error_based']['error_patterns_found'])}",
                        remediation="Implement input validation and parameterized queries; escape output for XSS",
                        evidence=resp.text[:800],
                        cwe=cwe,
                        owasp=owasp,
                        detection_method='multi_technique',
                        confidence=confidence,
                        poc=payload,
                        payload_type=payload_type,
                        exploitation_method=exploitation_method,
                        how_exploit_works=how_exploit_works,
                    )
                    
                    # Validate and enhance confidence with threat intelligence
                    vuln_dict = vuln.__dict__
                    threat_data = self.threat_intel.verify_finding_accuracy(vuln_dict)
                    enhanced_confidence = self.accuracy_validator.enhance_confidence(vuln_dict, threat_data)
                    vuln.confidence = enhanced_confidence
                    
                    # Set helper flags used by AI classifier
                    setattr(vuln, 'has_poc', True)
                    setattr(vuln, 'public_exploit', False)

                    self.vulnerabilities.append(vuln)
                    # Execute PoC exploit to capture response for verification
                    if self.auto_exploit:
                        color_logger.info(f"Auto-executing PoC for {vuln_type}", "EXPLOIT")
                        self._execute_poc(vuln)
                    color_logger.warning(f"Potential injection: {vuln_type}", "INJECT")
            except Exception as e:
                logger.debug(f"Error testing injection: {e}")
    
    def _crawl_site(self, start_url: str, max_depth: int, visited: Set[str]):
        """Crawl website to find more resources"""
        color_logger.info(f"Crawling site (depth: {max_depth})", "CRAWL")
        
        def crawl_recursive(url: str, depth: int):
            if depth == 0 or url in visited:
                return
            
            visited.add(url)
            
            try:
                resp = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
                soup = BeautifulSoup(resp.content, 'html.parser')
                
                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Only crawl same domain
                    if urlparse(absolute_url).netloc == urlparse(start_url).netloc:
                        if absolute_url not in visited:
                            crawl_recursive(absolute_url, depth - 1)
            except Exception as e:
                logger.debug(f"Error crawling {url}: {e}")
        
        crawl_recursive(start_url, max_depth)
    
    def check_ssl_certificate(self, url: str) -> Dict:
        """Check SSL certificate validity"""
        color_logger.info("Checking SSL certificate", "SSL")
        
        try:
            resp = self.session.head(url, timeout=self.timeout)
            
            # Basic SSL check - in production use ssl module
            if url.startswith('https'):
                return {
                    'valid': True,
                    'protocol': 'HTTPS',
                }
        except Exception as e:
            logger.error(f"SSL check failed: {e}")
        
        return {'valid': False}
    
    def check_caching_headers(self, url: str):
        """Check for insecure caching headers"""
        try:
            resp = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            
            cache_control = resp.headers.get('Cache-Control', '')
            if not cache_control or 'no-cache' not in cache_control.lower():
                vuln = Vulnerability(
                    name="Insecure Caching Configuration",
                    type="Security Misconfiguration",
                    url=url,
                    severity=RiskLevel.LOW,
                    description="Missing or insecure Cache-Control header",
                    remediation="Set Cache-Control: no-cache, no-store, must-revalidate",
                )
                self.vulnerabilities.append(vuln)
                color_logger.warning("Insecure cache configuration found", "CACHE")
        except Exception as e:
            logger.error(f"Cache header check failed: {e}")

    def _execute_poc(self, vuln: Vulnerability):
        """Execute PoC payload (where applicable) and capture response for reporting.

        Stores `poc_response` (snippet) and `poc_response_status` on the vulnerability object.
        This is a non-destructive GET-based execution that re-requests `vuln.url`.
        """
        if not vuln or not getattr(vuln, 'poc', None):
            return

        try:
            # Re-request the URL which should already contain the PoC payload when applicable
            resp = self.session.get(vuln.url, timeout=self.timeout, verify=self.verify_ssl)
            vuln.poc_response_status = getattr(resp, 'status_code', None)
            text = resp.text or ''
            # store a reasonable sized snippet
            vuln.poc_response = text[:2000]

            # If payload is reflected, raise confidence and mark PoC confirmed
            if vuln.poc and vuln.poc in text:
                vuln.confidence = min(1.0, (vuln.confidence or 0.0) + 0.1)
                setattr(vuln, 'poc_confirmed', True)
            else:
                setattr(vuln, 'poc_confirmed', False)

        except Exception as e:
            logger.debug(f"Error executing PoC for {vuln.url}: {e}")
            vuln.poc_response = f"Error executing PoC: {e}"
