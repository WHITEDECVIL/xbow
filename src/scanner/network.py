"""
Network Scanner Module - Host Discovery and Port Scanning
"""

import socket
import threading
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from queue import Queue
import subprocess
import json

from src.utils.logger import logger, color_logger
from src.utils.helpers import parse_port_range, run_command, check_command_exists


@dataclass
class HostInfo:
    """Information about discovered host"""
    ip: str
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    status: str = "up"
    open_ports: List[Dict] = field(default_factory=list)
    os_info: Optional[str] = None
    services: Dict = field(default_factory=dict)


@dataclass
class PortInfo:
    """Information about scanned port"""
    port: int
    protocol: str = "tcp"
    state: str = "closed"  # open, closed, filtered
    service: Optional[str] = None
    version: Optional[str] = None
    banner: Optional[str] = None


class NetworkScanner:
    """Advanced network scanner"""
    
    def __init__(self, timeout: int = 10, threads: int = 4):
        self.timeout = timeout
        self.threads = threads
        self.results = {}
        self.lock = threading.Lock()
        
        # Check for required tools
        self.has_nmap = check_command_exists('nmap')
    
    def ping_sweep(self, subnet: str) -> List[str]:
        """Discover live hosts in subnet"""
        color_logger.info(f"Starting ping sweep on {subnet}", "NETWORK")
        live_hosts = []
        
        if self.has_nmap:
            return self._ping_sweep_nmap(subnet)
        else:
            return self._ping_sweep_manual(subnet)
    
    def _ping_sweep_manual(self, subnet: str) -> List[str]:
        """Ping sweep without nmap"""
        import ipaddress
        
        live_hosts = []
        network = ipaddress.ip_network(subnet, strict=False)
        
        for ip in network.hosts():
            ip_str = str(ip)
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '1', ip_str],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    live_hosts.append(ip_str)
                    color_logger.success(f"Host found: {ip_str}", "PING")
            except Exception as e:
                logger.debug(f"Error pinging {ip_str}: {e}")
        
        return live_hosts
    
    def _ping_sweep_nmap(self, subnet: str) -> List[str]:
        """Ping sweep using nmap"""
        try:
            cmd = ['nmap', '-sn', subnet, '-oG', '-']
            returncode, stdout, _ = run_command(cmd, timeout=60)
            
            live_hosts = []
            for line in stdout.split('\n'):
                if 'Host:' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        ip = parts[1]
                        live_hosts.append(ip)
                        color_logger.success(f"Host found: {ip}", "NMAP")
            
            return live_hosts
        except Exception as e:
            logger.error(f"Nmap ping sweep failed: {e}")
            return []
    
    def scan_ports(self, target: str, ports: str = "1-1000") -> HostInfo:
        """Scan ports on target host"""
        color_logger.info(f"Scanning ports on {target}", "SCANNER")
        
        host_info = HostInfo(ip=target)
        
        if self.has_nmap:
            self._scan_ports_nmap(target, ports, host_info)
        else:
            self._scan_ports_manual(target, ports, host_info)
        
        return host_info
    
    def _scan_ports_manual(self, target: str, ports: str, host_info: HostInfo):
        """Manual port scanning without nmap"""
        port_list = parse_port_range(ports)
        
        queue = Queue()
        for port in port_list:
            queue.put(port)
        
        def worker():
            while not queue.empty():
                port = queue.get()
                self._check_port(target, port, host_info)
                queue.task_done()
        
        threads = []
        for _ in range(min(self.threads, len(port_list))):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
    
    def _check_port(self, host: str, port: int, host_info: HostInfo):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                port_info = PortInfo(port=port, state='open')
                service = socket.getservbyport(port)
                port_info.service = service
                
                with self.lock:
                    host_info.open_ports.append(port_info.__dict__)
                
                color_logger.success(f"Port {port}/{port_info.service} OPEN", "PORT")
        except Exception as e:
            logger.debug(f"Error checking port {port}: {e}")
    
    def _scan_ports_nmap(self, target: str, ports: str, host_info: HostInfo):
        """Port scanning using nmap"""
        try:
            cmd = [
                'nmap',
                '-p', ports,
                '-sV',  # Service version detection
                '-sC',  # Default scripts
                '--open',
                '-oX', '-',  # XML output
                target
            ]
            
            returncode, stdout, _ = run_command(cmd, timeout=300)
            
            # Parse XML output (simplified)
            self._parse_nmap_output(stdout, host_info)
        except Exception as e:
            logger.error(f"Nmap port scan failed: {e}")
    
    def _parse_nmap_output(self, xml_output: str, host_info: HostInfo):
        """Parse nmap XML output"""
        # Simplified parsing - in production, use XML parser
        for line in xml_output.split('\n'):
            if 'portid' in line:
                # Extract port information
                try:
                    if 'state="open"' in line:
                        # Extract port number
                        start = line.find('portid="')
                        if start != -1:
                            start += 8
                            end = line.find('"', start)
                            port = int(line[start:end])
                            
                            port_info = PortInfo(port=port, state='open')
                            host_info.open_ports.append(port_info.__dict__)
                            color_logger.success(f"Port {port} OPEN", "NMAP")
                except Exception as e:
                    logger.debug(f"Error parsing port: {e}")
    
    def service_detection(self, host: str, port: int) -> Optional[str]:
        """Detect service running on port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            sock.send(b"HELP\r\n")
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            return response[:100]
        except Exception as e:
            logger.debug(f"Error detecting service: {e}")
            return None
    
    def os_detection(self, target: str) -> Optional[str]:
        """Detect OS of target"""
        if not self.has_nmap:
            return None
        
        try:
            cmd = ['nmap', '-O', '--osscan-guess', target, '-oG', '-']
            returncode, stdout, _ = run_command(cmd, timeout=60)
            
            for line in stdout.split('\n'):
                if 'OS details' in line:
                    return line.split('OS details:')[1].strip()
            
            return None
        except Exception as e:
            logger.error(f"OS detection failed: {e}")
            return None
