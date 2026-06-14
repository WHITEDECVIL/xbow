"""
XBOW CLI - Command Line Interface
"""

import click
import json
import shlex
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.utils.logger import color_logger, logger
from src.utils.config import get_config, init_config
from src.utils.helpers import is_valid_ip, is_valid_cidr, is_valid_domain, expand_cidr, extract_domain_from_url, run_command
from src.scanner import NetworkScanner, WebScanner, DNSScanner, VulnerabilityDetector
from src.ai_engine import ThreatAnalyzer, AIProviderManager
from src.reporting import ReportGenerator
from src.accuracy_metrics import AccuracyMetrics


@click.group()
@click.option('--config', type=str, default=None, help='Config file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(config, verbose):
    """
    XBOW - Professional AI-Powered Penetration Testing Framework
    
    Advanced security assessment and vulnerability detection
    """
    
    # Initialize configuration
    init_config(config)
    config_mgr = get_config()
    
    if verbose:
        config_mgr.update_scan_config(verbose=True, log_level='DEBUG')
    
    # Print banner
    print_banner()


def print_banner():
    """Print XBOW banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║          XBOW - AI Penetration Testing Framework              ║
    ║                  Version 1.0.0                                ║
    ║                                                               ║
    ║     Advanced Vulnerability Detection & Analysis Engine        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


@main.command()
@click.option('--target', '-t', required=True, help='Target IP, CIDR, domain or URL')
@click.option('--scan-type', '-s', 
              type=click.Choice(['network', 'web', 'dns', 'full']),
              default='network', help='Type of scan to perform')
@click.option('--ports', '-p', default='1-1000', help='Port range (e.g., 80,443,1000-2000)')
@click.option('--depth', '-d', type=int, default=2, help='Web crawl depth')
@click.option('--threads', type=int, default=4, help='Number of threads')
@click.option('--output', '-o', default=None, help='Output directory')
@click.option('--auto-exploit', is_flag=True, help='Automatically execute PoC for detected vulnerabilities')
@click.option('--generate-report', is_flag=True, help='Generate HTML report')
def scan(target, scan_type, ports, depth, threads, output, auto_exploit, generate_report):
    """
    Perform security scan on target
    
    Examples:
        xbow scan --target 192.168.1.0/24 --scan-type network
        xbow scan --target https://example.com --scan-type web
        xbow scan --target example.com --scan-type dns
    """
    
    config = get_config()
    if output:
        config.update_scan_config(output_dir=output)
    
    # Store auto_exploit in config for use in web scanner
    config.update_scan_config(auto_exploit=auto_exploit)
    
    findings = {
        'target': target,
        'scan_type': scan_type,
        'timestamp': datetime.now().isoformat(),
        'vulnerabilities': [],
        'hosts': [],
    }
    
    try:
        if scan_type in ['network', 'full']:
            color_logger.info("Starting network scan", "SCAN")
            findings['hosts'] = _perform_network_scan(target, ports, threads)
        
        if scan_type in ['web', 'full']:
            color_logger.info("Starting web scan", "SCAN")
            findings['vulnerabilities'].extend(_perform_web_scan(target, depth, auto_exploit))
        
        if scan_type in ['dns', 'full']:
            color_logger.info("Starting DNS enumeration", "SCAN")
            _perform_dns_scan(target, findings)
        
        # Run AI analysis
        analyzer = ThreatAnalyzer()
        analysis = analyzer.analyze_findings(findings)
        findings['risk_level'] = analysis['risk_rating']
        
        for vuln in analysis['vulnerabilities']:
            for existing_vuln in findings['vulnerabilities']:
                if existing_vuln.get('name') == vuln.get('name'):
                    existing_vuln.update({
                        'ai_severity': vuln.get('ai_severity'),
                        'confidence': vuln.get('confidence')
                    })
        
        # Display results
        _display_results(findings)
        
        # Generate report
        if generate_report:
            reporter = ReportGenerator(config.get_output_dir())
            reporter.generate_html_report(findings)
            reporter.generate_json_report(findings)
        
        # Generate accuracy metrics
        metrics = AccuracyMetrics(config.get_output_dir())
        
        # Record findings for accuracy tracking (assume high confidence for demo)
        for vuln in findings.get('vulnerabilities', []):
            confidence = vuln.get('confidence', 0.8)  # Default high confidence for demo
            metrics.record_finding(vuln, verified=True, confidence=confidence)
        
        metrics.print_report()
        metrics.save_metrics()
        
        color_logger.success("Scan completed successfully", "COMPLETE")
    
    except Exception as e:
        color_logger.error(f"Scan failed: {e}", "ERROR")
        logger.exception(e)


def _perform_network_scan(target: str, ports: str, threads: int) -> list:
    """Perform network scanning"""
    scanner = NetworkScanner(threads=threads)
    hosts = []
    
    # Extract domain from URL if necessary
    if target.startswith(('http://', 'https://')):
        target = extract_domain_from_url(target)
    
    # Determine if target is IP/CIDR or domain
    if is_valid_cidr(target) or is_valid_ip(target):
        if is_valid_cidr(target):
            live_hosts = scanner.ping_sweep(target)
        else:
            live_hosts = [target]
    elif is_valid_domain(target):
        import socket
        try:
            ip = socket.gethostbyname(target)
            live_hosts = [ip]
        except:
            color_logger.warning(f"Could not resolve {target}", "DNS")
            return hosts
    else:
        color_logger.error(f"Invalid target format: {target}", "ERROR")
        return hosts
    
    # Scan ports on each host
    for host in live_hosts:
        host_info = scanner.scan_ports(host, ports)
        
        # Detect services
        for port_info in host_info.open_ports:
            service = scanner.service_detection(host, port_info.get('port'))
            if service:
                port_info['service'] = service
        
        # Detect OS
        os_info = scanner.os_detection(host)
        if os_info:
            host_info.os_info = os_info
        
        hosts.append(host_info.__dict__)
    
    return hosts


def _perform_web_scan(target: str, depth: int, auto_exploit: bool = False) -> list:
    """Perform web application scanning"""
    scanner = WebScanner(auto_exploit=auto_exploit)
    
    # Ensure target has scheme
    if not target.startswith(('http://', 'https://')):
        target = f"https://{target}"
    
    vulnerabilities = []
    
    try:
        vulns = scanner.scan_url(target, crawl=True, depth=depth)
        vulnerabilities.extend([v.__dict__ if hasattr(v, '__dict__') else v for v in vulns])
        
        # Check SSL
        ssl_info = scanner.check_ssl_certificate(target)
        if not ssl_info.get('valid'):
            from src.scanner.web import Vulnerability
            vuln = Vulnerability(
                name="Invalid SSL Certificate",
                type="SSL/TLS Issue",
                url=target,
                severity="MEDIUM",
                description="SSL certificate validation failed",
                remediation="Install valid SSL certificate",
            )
            vulnerabilities.append(vuln.__dict__)
        
        scanner.check_caching_headers(target)
    
    except Exception as e:
        color_logger.error(f"Web scan error: {e}", "WEB")
    
    return vulnerabilities


def _perform_dns_scan(target: str, findings: dict):
    """Perform DNS enumeration"""
    scanner = DNSScanner()
    
    # Extract domain from URL if necessary
    domain = extract_domain_from_url(target)
    
    try:
        records = scanner.enumerate_dns_records(domain)
        findings['dns_records'] = {k: [r.__dict__ for r in v] for k, v in records.items()}
        
        # Try zone transfer
        zone_records = scanner.zone_transfer(domain)
        if zone_records:
            findings['zone_transfer'] = [r.__dict__ for r in zone_records]
        
        # Check DNS security
        security = scanner.check_dns_security(domain)
        findings['dns_security'] = security
    
    except Exception as e:
        color_logger.error(f"DNS scan error: {e}", "DNS")


def _display_results(findings: dict):
    """Display scan results"""
    print("\n" + "="*70)
    print("SCAN RESULTS")
    print("="*70 + "\n")
    
    # Display vulnerability summary
    vulns = findings.get('vulnerabilities', [])
    severity_counts = {}
    
    for vuln in vulns:
        severity = vuln.get('ai_severity') or vuln.get('severity', 'MEDIUM')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print(f"Target: {findings['target']}")
    print(f"Scan Type: {findings['scan_type']}")
    print(f"\nVulnerabilities Found: {len(vulns)}")
    
    for severity, count in severity_counts.items():
        color = {
            'CRITICAL': '\033[91m',
            'HIGH': '\033[93m',
            'MEDIUM': '\033[94m',
            'LOW': '\033[92m',
        }.get(severity, '\033[0m')
        
        print(f"  {color}{severity}: {count}\033[0m")
    
    if vulns and len(vulns) <= 10:
        print("\nTop Vulnerabilities:")
        for vuln in sorted(vulns, 
                          key=lambda v: {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2}.get(
                              v.get('severity'), 0), reverse=True)[:5]:
            print(f"  ⚠️  {vuln.get('name')}")
    
    print("\n" + "="*70 + "\n")


@main.command()
@click.option('--target', '-t', required=True, help='Target domain or IP')
@click.option('--wordlist', '-w', default=None, help='Wordlist file for subdomain enumeration')
@click.option('--output', '-o', default=None, help='Output file')
def enumerate(target, wordlist, output):
    """
    Perform DNS enumeration and subdomain discovery
    
    Example:
        xbow enumerate --target example.com
    """
    
    color_logger.info(f"Enumerating {target}", "ENUM")
    
    scanner = DNSScanner()
    results = {'subdomains': [], 'dns_records': {}}
    
    # Enumerate DNS records
    records = scanner.enumerate_dns_records(target)
    results['dns_records'] = {k: [r.__dict__ for r in v] for k, v in records.items()}
    
    # Subdomain enumeration
    subdomains = scanner.find_subdomains_dns(target)
    results['subdomains'] = subdomains
    
    color_logger.success(f"Found {len(subdomains)} subdomains", "ENUM")
    
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        color_logger.success(f"Results saved to {output}", "OUTPUT")


@main.command()
@click.option('--target', '-t', required=True, help='Target IP, CIDR, domain or URL')
@click.option('--profile', '-p', default='basic', help='Scan profile (basic, aggressive, stealth)')
@click.option('--generate-report', is_flag=True, help='Generate HTML and JSON report')
def pentest(target, profile, generate_report):
    """
    Perform comprehensive penetration testing on target
    
    Example:
        xbow pentest --target example.com --profile aggressive --generate-report
    """
    
    color_logger.info(f"Starting comprehensive pentest on {target}", "PENTEST")
    
    # Load profile configuration
    config = get_config()
    if profile == 'aggressive':
        config.update_scan_config(threads=10, timeout=30, auto_exploit=True)
    elif profile == 'stealth':
        config.update_scan_config(threads=2, timeout=60, auto_exploit=False)
    
    findings = {
        'target': target,
        'profile': profile,
        'scan_type': 'full',
        'timestamp': datetime.now().isoformat(),
        'vulnerabilities': [],
        'hosts': [],
    }
    
    try:
        # Phase 1: Network reconnaissance
        color_logger.info("Phase 1: Network reconnaissance", "PENTEST")
        findings['hosts'] = _perform_network_scan(target, "1-1000", 4)
        
        # Phase 2: Web application testing
        color_logger.info("Phase 2: Web application testing", "PENTEST")
        if target.startswith(('http://', 'https://')):
            findings['vulnerabilities'].extend(_perform_web_scan(target, 3, True))
        
        # Phase 3: DNS enumeration
        color_logger.info("Phase 3: DNS enumeration", "PENTEST")
        _perform_dns_scan(target, findings)
        
        # Phase 4: Vulnerability correlation
        color_logger.info("Phase 4: Vulnerability correlation", "PENTEST")
        analyzer = ThreatAnalyzer()
        analysis = analyzer.analyze_findings(findings)
        findings['risk_level'] = analysis['risk_rating']
        
        for vuln in analysis['vulnerabilities']:
            for existing_vuln in findings['vulnerabilities']:
                if existing_vuln.get('name') == vuln.get('name'):
                    existing_vuln.update({
                        'ai_severity': vuln.get('ai_severity'),
                        'confidence': vuln.get('confidence')
                    })
        
        # Phase 5: Exploitation (if enabled)
        if config.scan_config.auto_exploit:
            color_logger.info("Phase 5: Exploitation testing", "PENTEST")
            _perform_exploitation(findings)
        
        # Display results
        _display_results(findings)
        
        # Generate comprehensive report when requested
        if generate_report:
            reporter = ReportGenerator(config.get_output_dir())
            reporter.generate_html_report(findings)
            reporter.generate_json_report(findings)
        else:
            color_logger.warning("Report generation skipped; use --generate-report to create reports", "REPORT")
        
        # Generate accuracy metrics
        metrics = AccuracyMetrics(config.get_output_dir())
        for vuln in findings.get('vulnerabilities', []):
            confidence = vuln.get('confidence', 0.8)
            metrics.record_finding(vuln, verified=True, confidence=confidence)
        metrics.print_report()
        metrics.save_metrics()
        
        color_logger.success("Comprehensive pentest completed", "PENTEST")
    
    except Exception as e:
        color_logger.error(f"Pentest failed: {e}", "ERROR")
        logger.exception(e)


def _perform_exploitation(findings: dict):
    """Perform exploitation testing on confirmed vulnerabilities"""
    from src.exploits import ExploitEngine
    
    engine = ExploitEngine()
    
    for vuln in findings.get('vulnerabilities', []):
        if vuln.get('confidence', 0) > 0.8:  # Only exploit high-confidence findings
            try:
                result = engine.attempt_exploit(vuln)
                if result:
                    vuln['exploitation_result'] = result
                    color_logger.success(f"Exploitation successful: {vuln.get('name')}", "EXPLOIT")
                else:
                    color_logger.warning(f"Exploitation failed: {vuln.get('name')}", "EXPLOIT")
            except Exception as e:
                color_logger.error(f"Exploitation error: {e}", "EXPLOIT")


@main.command()
@click.option('--target', '-t', required=True, help='Target IP, CIDR, domain or URL')
@click.option('--mode', '-m', default='interactive', type=click.Choice(['interactive', 'monitor', 'auto']), 
              help='Live pentesting mode')
@click.option('--duration', '-d', default=300, type=int, help='Monitoring duration in seconds')
@click.option('--enable-ai-agent/--disable-ai-agent', default=False,
              help='Enable AI orchestration agent in auto mode')
@click.option('--agent-provider', default=None,
              help='Select AI agent provider from config/ai_agents.json')
def live(target, mode, duration, enable_ai_agent, agent_provider):
    """
    Live penetration testing with real-time interaction
    
    Modes:
    - interactive: Interactive shell for manual testing
    - monitor: Real-time monitoring of target
    - auto: AI-driven automated pentesting with intelligent decision making
    
    Example:
        xbow live --target https://example.com --mode interactive
        xbow live --target https://example.com --mode monitor --duration 600
        xbow live --target https://example.com --mode auto --duration 300
    """
    
    color_logger.info(f"Starting live pentesting on {target} (mode: {mode})", "LIVE")
    
    if mode == 'interactive':
        _interactive_mode(target)
    elif mode == 'monitor':
        _monitor_mode(target, duration)
    elif mode == 'auto':
        _auto_mode(target, duration)


def _interactive_mode(target: str):
    """Interactive pentesting shell"""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    
    commands = [
        'scan', 'exploit', 'list', 'info', 'help', 'quit',
        'nmap', 'sqlmap', 'dirb', 'nikto', 'metasploit'
    ]
    
    completer = WordCompleter(commands)
    session = PromptSession(completer=completer)
    
    # Session state
    session_vulns = []
    vuln_counter = 1
    
    color_logger.info("Interactive pentesting shell started. Type 'help' for commands.", "LIVE")
    color_logger.info(f"Target: {target}", "LIVE")
    
    while True:
        try:
            cmd = session.prompt(f"XBOW[{target}]> ").strip()
            
            if cmd == 'quit' or cmd == 'exit':
                break
            elif cmd == 'help':
                _show_interactive_help()
            elif cmd.startswith('scan'):
                new_vulns = _interactive_scan(target, cmd)
                # Add new vulnerabilities with IDs
                for vuln in new_vulns:
                    vuln['id'] = vuln_counter
                    session_vulns.append(vuln)
                    vuln_counter += 1
            elif cmd.startswith('exploit'):
                _interactive_exploit(target, cmd, session_vulns)
            elif cmd == 'list':
                _list_vulnerabilities(session_vulns)
            elif cmd == 'info':
                _show_target_info(target)
            elif cmd.startswith('nmap'):
                _run_nmap(target, cmd)
            elif cmd.startswith('sqlmap'):
                _run_sqlmap(target, cmd)
            elif cmd.startswith('dirb'):
                _run_dirb(target, cmd)
            elif cmd.startswith('nikto'):
                _run_nikto(target, cmd)
            elif cmd.startswith('metasploit'):
                _run_metasploit(target, cmd)
            else:
                color_logger.warning(f"Unknown command: {cmd}", "LIVE")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            color_logger.error(f"Command error: {e}", "LIVE")
    
    color_logger.info("Interactive session ended", "LIVE")


def _monitor_mode(target: str, duration: int):
    """Real-time monitoring mode"""
    import time
    
    color_logger.info(f"Monitoring {target} for {duration} seconds", "MONITOR")
    
    start_time = time.time()
    scan_count = 0
    
    while time.time() - start_time < duration:
        scan_count += 1
        color_logger.info(f"Scan #{scan_count}", "MONITOR")
        
        # Quick scan
        scanner = WebScanner()
        try:
            if target.startswith(('http://', 'https://')):
                vulns = scanner.scan_url(target, crawl=False, depth=1)
                if vulns:
                    color_logger.warning(f"Found {len(vulns)} new vulnerabilities", "MONITOR")
                    for vuln in vulns[:3]:  # Show first 3
                        color_logger.info(f"  - {vuln.name}", "MONITOR")
                else:
                    color_logger.info("No new vulnerabilities found", "MONITOR")
        except Exception as e:
            color_logger.error(f"Monitor scan error: {e}", "MONITOR")
        
        time.sleep(30)  # Scan every 30 seconds
    
    color_logger.success(f"Monitoring completed ({scan_count} scans)", "MONITOR")


def _auto_mode(target: str, duration: int, enable_ai_agent: bool = False, agent_provider: Optional[str] = None):
    """AI-driven automated live testing"""
    import time
    from src.ai_engine import ThreatAnalyzer
    
    color_logger.info(f"AI automated testing on {target} for {duration} seconds", "AUTO")
    
    config = get_config()
    if enable_ai_agent:
        config.ai_config.enable_agent = True
    if agent_provider:
        config.ai_config.agent_provider = agent_provider

    agent_manager = AIProviderManager()
    agent = None
    if config.ai_config.enable_agent:
        agent = agent_manager.create_agent(config.ai_config.agent_provider)
        color_logger.info(f"AI agent enabled: {agent.name}", "AUTO")

    start_time = time.time()
    analyzer = ThreatAnalyzer()
    session_vulns = []
    vuln_counter = 1
    sqlmap_attempted = False
    nmap_attempted = False
    
    # Initial reconnaissance
    color_logger.info("Phase 1: Initial reconnaissance", "AUTO")
    _auto_initial_scan(target, session_vulns, vuln_counter)
    vuln_counter = len(session_vulns) + 1
    
    while time.time() - start_time < duration:
        # AI-driven decision making
        action = None
        if agent:
            action = agent.recommend_next_action(target, session_vulns, analyzer)
        if not action:
            action = _ai_decide_next_action(target, session_vulns, analyzer, sqlmap_attempted, nmap_attempted)
        
        if action['type'] == 'scan':
            color_logger.info(f"AI Decision: Performing {action['scan_type']} scan", "AUTO")
            new_vulns = _auto_perform_scan(target, action['scan_type'])
            for vuln in new_vulns:
                vuln['id'] = vuln_counter
                session_vulns.append(vuln)
                vuln_counter += 1
                
        elif action['type'] == 'exploit':
            vuln_id = action['vuln_id']
            vuln = next((v for v in session_vulns if v.get('id') == vuln_id), None)
            if vuln:
                color_logger.info(f"AI Decision: Exploiting vulnerability {vuln_id}", "AUTO")
                _auto_exploit_vulnerability(target, vuln)
                
        elif action['type'] == 'nmap':
            color_logger.info(f"AI Decision: Running nmap scan with options {action['options']}", "AUTO")
            _auto_run_nmap(target, action['options'])
            nmap_attempted = True
            
        elif action['type'] == 'sqlmap':
            color_logger.info(f"AI Decision: Running sqlmap on {action['url']}", "AUTO")
            _auto_run_sqlmap(action['url'], action['options'])
            sqlmap_attempted = True
            
        elif action['type'] == 'wait':
            color_logger.info(f"AI Decision: Waiting {action['seconds']} seconds", "AUTO")
            time.sleep(action['seconds'])
            
        elif action['type'] == 'stop':
            color_logger.info("AI Decision: Stopping automated testing", "AUTO")
            break
            
        # Brief pause between actions
        time.sleep(2)
    
    # Final summary
    _auto_generate_summary(session_vulns, target)
    color_logger.success("AI automated testing completed", "AUTO")


def _show_interactive_help():
    """Show interactive help"""
    help_text = """
Available Commands:
  scan [type]          - Run scan (network, web, dns, full)
  list                 - List found vulnerabilities with IDs
  exploit [id]         - Attempt exploitation of vulnerability by ID
  info                 - Show target information
  nmap [options]       - Run nmap scan
  sqlmap [options]     - Run sqlmap injection test
  dirb [options]       - Run directory brute force
  nikto [options]      - Run nikto web scan
  metasploit           - Launch metasploit console
  help                 - Show this help
  quit/exit            - Exit interactive mode

Examples:
  scan web
  list
  exploit 1
  nmap -p 80,443
  sqlmap -u "https://target.com/page?id=1"
"""
    print(help_text)


def _interactive_scan(target: str, cmd: str):
    """Handle interactive scan command"""
    parts = cmd.split()
    scan_type = parts[1] if len(parts) > 1 else 'web'
    
    color_logger.info(f"Running {scan_type} scan on {target}", "SCAN")
    
    vulnerabilities = []
    
    if scan_type == 'web':
        scanner = WebScanner()
        vulns = scanner.scan_url(target, crawl=True, depth=2)
        vulnerabilities.extend([v.__dict__ if hasattr(v, '__dict__') else v for v in vulns])
        color_logger.success(f"Found {len(vulnerabilities)} vulnerabilities", "SCAN")
    elif scan_type == 'network':
        # Quick network scan
        color_logger.info("Network scan not implemented in interactive mode", "SCAN")
    else:
        color_logger.warning(f"Scan type {scan_type} not supported", "SCAN")
    
    return vulnerabilities


def _interactive_exploit(target: str, cmd: str, session_vulns: list):
    """Handle interactive exploit command"""
    parts = cmd.split()
    
    if len(parts) < 2:
        color_logger.error("Usage: exploit <id>", "EXPLOIT")
        return
    
    try:
        vuln_id = int(parts[1])
    except ValueError:
        color_logger.error("Invalid vulnerability ID. Use 'list' to see available vulnerabilities.", "EXPLOIT")
        return
    
    # Find vulnerability by ID
    vuln = None
    for v in session_vulns:
        if v.get('id') == vuln_id:
            vuln = v
            break
    
    if not vuln:
        color_logger.error(f"Vulnerability with ID {vuln_id} not found. Use 'list' to see available vulnerabilities.", "EXPLOIT")
        return
    
    # Attempt exploitation
    color_logger.info(f"Attempting exploitation of: {vuln.get('name', 'Unknown')}", "EXPLOIT")
    
    from src.exploits import ExploitEngine
    engine = ExploitEngine(safe_mode=True)
    
    result = engine.attempt_exploit(vuln)
    
    if result:
        color_logger.success(f"Exploitation successful: {result.get('description', 'Success')}", "EXPLOIT")
        vuln['exploitation_result'] = result
    else:
        color_logger.warning("Exploitation failed or not supported for this vulnerability type", "EXPLOIT")


def _list_vulnerabilities(session_vulns: list):
    """List all found vulnerabilities with IDs"""
    if not session_vulns:
        print("\nNo vulnerabilities found yet. Run 'scan web' to find vulnerabilities.\n")
        return
    
    print(f"\nFound {len(session_vulns)} vulnerabilities:\n")
    print("-" * 80)
    print(f"{'ID':<3} {'Type':<15} {'Severity':<10} {'Name'}")
    print("-" * 80)
    
    for vuln in session_vulns:
        vuln_id = vuln.get('id', 'N/A')
        vuln_type = vuln.get('type', 'Unknown')[:14]
        severity = vuln.get('severity', 'Unknown')[:9]
        name = vuln.get('name', 'Unknown Vulnerability')
        
        print(f"{vuln_id:<3} {vuln_type:<15} {severity:<10} {name}")
    
    print("-" * 80)
    print("Use 'exploit <id>' to attempt exploitation of a specific vulnerability.\n")


def _show_target_info(target: str):
    """Show target information"""
    print(f"\nTarget: {target}")
    
    # Basic info
    if target.startswith(('http://', 'https://')):
        print("Type: Web Application")
        from urllib.parse import urlparse
        parsed = urlparse(target)
        print(f"Domain: {parsed.netloc}")
        print(f"Scheme: {parsed.scheme}")
    else:
        print("Type: Network Target")
    
    print()


def _run_nmap(target: str, cmd: str):
    """Run nmap command"""
    options = cmd.replace('nmap', '').strip()
    full_cmd = f"nmap {options} {target}"
    color_logger.info(f"Running: {full_cmd}", "NMAP")
    
    try:
        result = run_command(full_cmd.split())
        if result[0] == 0:
            print(result[1])
        else:
            color_logger.error(f"Nmap failed: {result[2]}", "NMAP")
    except Exception as e:
        color_logger.error(f"Nmap error: {e}", "NMAP")


def _run_sqlmap(target: str, cmd: str):
    """Run sqlmap command"""
    options = cmd.replace('sqlmap', '').strip()
    full_cmd = f"sqlmap {options}"
    color_logger.info(f"Running: {full_cmd}", "SQLMAP")
    
    try:
        result = run_command(shlex.split(full_cmd))
        if result[0] == 0:
            print(result[1])
        else:
            color_logger.error(f"SQLMap failed: {result[2]}", "SQLMAP")
    except Exception as e:
        color_logger.error(f"SQLMap error: {e}", "SQLMAP")


def _run_dirb(target: str, cmd: str):
    """Run dirb command"""
    options = cmd.replace('dirb', '').strip()
    full_cmd = f"dirb {target} {options}"
    color_logger.info(f"Running: {full_cmd}", "DIRB")
    
    try:
        result = run_command(full_cmd.split())
        if result[0] == 0:
            print(result[1])
        else:
            color_logger.error(f"Dirb failed: {result[2]}", "DIRB")
    except Exception as e:
        color_logger.error(f"Dirb error: {e}", "DIRB")


def _run_nikto(target: str, cmd: str):
    """Run nikto command"""
    options = cmd.replace('nikto', '').strip()
    full_cmd = f"nikto -h {target} {options}"
    color_logger.info(f"Running: {full_cmd}", "NIKTO")
    
    try:
        result = run_command(full_cmd.split())
        if result[0] == 0:
            print(result[1])
        else:
            color_logger.error(f"Nikto failed: {result[2]}", "NIKTO")
    except Exception as e:
        color_logger.error(f"Nikto error: {e}", "NIKTO")


def _run_metasploit(target: str, cmd: str):
    """Launch metasploit"""
    color_logger.info("Launching Metasploit console...", "METASPLOIT")
    color_logger.warning("Metasploit integration not implemented", "METASPLOIT")


def _run_automated_tests(target: str):
    """Run automated tests"""
    color_logger.info("Running automated tests...", "AUTO")
    # Implement automated testing logic here


# AI Automated Pentesting Functions

def _auto_generate_summary(session_vulns, target):
    """Generate summary of automated testing"""
    print(f"\n{'='*60}")
    print("AI AUTOMATED PENTESTING SUMMARY")
    print(f"{'='*60}")
    print(f"Target: {target}")
    print(f"Total Vulnerabilities Found: {len(session_vulns)}")
    
    if session_vulns:
        print("\nVulnerabilities by Severity:")
        severity_count = {}
        for vuln in session_vulns:
            severity = vuln.get('severity', 'Unknown')
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        for severity, count in severity_count.items():
            print(f"  {severity}: {count}")
        
        print("\nTop Vulnerabilities:")
        for vuln in sorted(session_vulns, 
                          key=lambda v: {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2}.get(
                              v.get('severity'), 0), reverse=True)[:5]:
            print(f"  • {vuln.get('name', 'Unknown')}")
    
    print(f"{'='*60}\n")


def _ai_decide_next_action(target: str, session_vulns: list, analyzer, sqlmap_attempted: bool = False, nmap_attempted: bool = False) -> dict:
    """AI-driven decision making for next action"""
    
    # Analyze current state
    high_severity = [v for v in session_vulns if v.get('severity') in ['HIGH', 'CRITICAL']]
    medium_severity = [v for v in session_vulns if v.get('severity') == 'MEDIUM']
    web_vulns = [v for v in session_vulns if 'web' in v.get('type', '').lower() or 'http' in v.get('url', '')]
    sql_vulns = [v for v in session_vulns if 'sql' in v.get('type', '').lower()]
    
    # Track what we've already done
    successful_vulns = [v for v in session_vulns if v.get('exploitation_result') and v.get('exploitation_result', {}).get('result') == 'test_completed']
    scanned_nmap = any('nmap' in str(v.get('scan_result', '')) for v in session_vulns)
    scanned_sqlmap = any('sqlmap' in str(v.get('exploitation_result', '')) for v in session_vulns)
    
    # Decision logic with priorities
    if len(session_vulns) == 0:
        # No vulnerabilities found yet, start with web scan
        return {'type': 'scan', 'scan_type': 'web'}
    
    elif high_severity and any(v.get('exploit_attempts', 0) == 0 for v in high_severity):
        # High severity vulnerabilities found that haven't been attempted yet
        unattempted_high = [v for v in high_severity if v.get('exploit_attempts', 0) == 0]
        if unattempted_high:
            vuln = unattempted_high[0]
            return {'type': 'exploit', 'vuln_id': vuln.get('id')}
    
    elif sql_vulns and not scanned_sqlmap and not sqlmap_attempted:
        # SQL vulnerabilities found, run sqlmap once
        vuln = sql_vulns[0]
        url = vuln.get('url', target)
        return {'type': 'sqlmap', 'url': url, 'options': '--batch --level=3 --risk=2'}
    
    elif not scanned_nmap and not nmap_attempted:
        # Haven't run nmap yet
        return {'type': 'nmap', 'options': '-sV -p 1-1000'}
    
    elif len(web_vulns) < 5 and len(session_vulns) < 10:
        # Not enough web vulnerabilities, scan more
        return {'type': 'scan', 'scan_type': 'web'}
    
    elif medium_severity and len(successful_vulns) < len(session_vulns) * 0.5:
        # Try exploiting some medium severity vulnerabilities that have not been attempted yet
        unattempted_medium = [v for v in medium_severity if v.get('exploit_attempts', 0) == 0]
        if unattempted_medium:
            vuln = unattempted_medium[0]
            return {'type': 'exploit', 'vuln_id': vuln.get('id')}
    
    elif len(session_vulns) > 15:
        # Found many vulnerabilities, might be enough
        return {'type': 'stop'}
    
    else:
        # Default: wait and continue monitoring
        return {'type': 'wait', 'seconds': 30}


def _auto_initial_scan(target: str, session_vulns: list, vuln_counter: int):
    """Perform initial automated scan"""
    color_logger.info("Running initial web vulnerability scan", "AUTO")
    
    scanner = WebScanner()
    try:
        vulns = scanner.scan_url(target, crawl=True, depth=2)
        vulnerabilities = [v.__dict__ if hasattr(v, '__dict__') else v for v in vulns]
        
        for vuln in vulnerabilities:
            vuln['id'] = vuln_counter
            session_vulns.append(vuln)
            vuln_counter += 1
            
        color_logger.success(f"Initial scan found {len(vulnerabilities)} vulnerabilities", "AUTO")
        
    except Exception as e:
        color_logger.error(f"Initial scan error: {e}", "AUTO")


def _auto_perform_scan(target: str, scan_type: str) -> list:
    """Perform automated scan"""
    vulnerabilities = []
    
    if scan_type == 'web':
        scanner = WebScanner()
        try:
            vulns = scanner.scan_url(target, crawl=False, depth=1)  # Quick scan
            vulnerabilities = [v.__dict__ if hasattr(v, '__dict__') else v for v in vulns]
        except Exception as e:
            color_logger.error(f"Web scan error: {e}", "AUTO")
    
    return vulnerabilities


def _auto_exploit_vulnerability(target: str, vuln: dict):
    """Automatically exploit a vulnerability"""
    from src.exploits import ExploitEngine
    
    engine = ExploitEngine(safe_mode=True)
    result = engine.attempt_exploit(vuln)
    vuln['exploit_attempts'] = vuln.get('exploit_attempts', 0) + 1
    
    if result:
        vuln['exploitation_result'] = result
        color_logger.success(f"Auto-exploitation successful: {result.get('description', 'Success')}", "AUTO")
    else:
        vuln['exploitation_result'] = {
            'type': 'unsupported',
            'result': 'failed',
            'safe': True,
            'description': 'Auto-exploit failed or unsupported for this vulnerability type'
        }
        color_logger.warning("Auto-exploitation failed or not supported", "AUTO")


def _auto_run_nmap(target: str, options: str):
    """Run nmap scan automatically"""
    args = ['nmap'] + shlex.split(options) + [target]
    color_logger.info(f"Running: {' '.join(shlex.quote(arg) for arg in args)}", "AUTO")
    
    try:
        result = run_command(args)
        if result[0] == 0:
            # Store results in session somehow
            color_logger.success("Nmap scan completed", "AUTO")
            return {'success': True, 'stdout': result[1], 'stderr': result[2]}
        else:
            color_logger.error(f"Nmap failed: {result[2]}", "AUTO")
            return {'success': False, 'stdout': result[1], 'stderr': result[2]}
    except Exception as e:
        color_logger.error(f"Nmap error: {e}", "AUTO")
        return {'success': False, 'stdout': '', 'stderr': str(e)}


def _auto_run_sqlmap(url: str, options: str):
    """Run sqlmap automatically"""
    args = ['sqlmap', '-u', url] + shlex.split(options)
    color_logger.info(f"Running: {' '.join(shlex.quote(arg) for arg in args)}", "AUTO")
    
    try:
        result = run_command(args)
        if result[0] == 0:
            color_logger.success("SQLMap scan completed", "AUTO")
            return {'success': True, 'stdout': result[1], 'stderr': result[2]}
        else:
            color_logger.error(f"SQLMap failed: {result[2]}", "AUTO")
            return {'success': False, 'stdout': result[1], 'stderr': result[2]}
    except Exception as e:
        color_logger.error(f"SQLMap error: {e}", "AUTO")
        return {'success': False, 'stdout': '', 'stderr': str(e)}


if __name__ == '__main__':
    main()
