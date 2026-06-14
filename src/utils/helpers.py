"""
Helper Utilities Module
"""

import socket
import ipaddress
from typing import List, Tuple, Optional
import subprocess
import json
from datetime import datetime
from urllib.parse import urlparse


def is_valid_ip(ip: str) -> bool:
    """Validate IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_cidr(cidr: str) -> bool:
    """Validate CIDR notation"""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def expand_cidr(cidr: str) -> List[str]:
    """Expand CIDR notation to list of IPs"""
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        return []


def is_valid_domain(domain: str) -> bool:
    """Validate domain name"""
    try:
        socket.gethostbyname(domain)
        return True
    except (socket.gaierror, socket.error):
        return False


def extract_domain_from_url(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    except:
        return url


def parse_port_range(port_spec: str) -> List[int]:
    """Parse port range specification (e.g., '80,443,1000-2000')"""
    ports = []
    
    for part in port_spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    
    return sorted(list(set(ports)))


def is_valid_ip(ip: str) -> bool:
    """Validate IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_cidr(cidr: str) -> bool:
    """Validate CIDR notation"""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def expand_cidr(cidr: str) -> List[str]:
    """Expand CIDR notation to list of IPs"""
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        return []


def is_valid_domain(domain: str) -> bool:
    """Validate domain name"""
    try:
        socket.gethostbyname(domain)
        return True
    except (socket.gaierror, socket.error):
        return False


def parse_port_range(port_spec: str) -> List[int]:
    """Parse port range specification (e.g., '80,443,1000-2000')"""
    ports = []
    
    for part in port_spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    
    return sorted(list(set(ports)))


def format_timestamp(dt: datetime = None) -> str:
    """Format datetime to string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def run_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    """Run system command and return (return_code, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return -1, "", str(e)


def check_command_exists(cmd: str) -> bool:
    """Check if command exists in system"""
    returncode, _, _ = run_command(['which', cmd])
    return returncode == 0


def safe_json_loads(data: str, default: dict = None):
    """Safely load JSON with default fallback"""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        return default or {}


class RiskLevel:
    """Risk/Severity level constants"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"
    
    SEVERITY_MAP = {
        "CRITICAL": 5,
        "HIGH": 4,
        "MEDIUM": 3,
        "LOW": 2,
        "INFO": 1,
    }


class Colors:
    """ANSI color codes"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
