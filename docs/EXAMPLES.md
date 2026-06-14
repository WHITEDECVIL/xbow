"""
Example usage and advanced scenarios for XBOW
"""

# Example 1: Basic Network Scan
"""
Command:
    xbow scan --target 192.168.1.0/24 --scan-type network --threads 4

This will:
1. Perform ping sweep to find live hosts
2. Scan top 1000 TCP ports on each host
3. Detect running services
4. Attempt OS detection
5. Display results
"""

# Example 2: Web Application Penetration Test
"""
Command:
    xbow scan --target https://example.com --scan-type web --depth 3 --generate-report

This will:
1. Analyze security headers
2. Check for common sensitive paths
3. Test for injection vulnerabilities
4. Crawl the website (3 levels deep)
5. Check SSL/TLS configuration
6. Generate HTML and JSON reports
"""

# Example 3: DNS Enumeration
"""
Command:
    xbow enumerate --target example.com --output subdomains.json

This will:
1. Query all DNS record types
2. Attempt zone transfer
3. Enumerate subdomains
4. Perform reverse DNS lookups
5. Check DNSSEC configuration
"""

# Example 4: Aggressive Full Pentest
"""
Command:
    xbow scan --target example.com --scan-type full --profile aggressive --generate-report

This will:
1. Perform network reconnaissance
2. Scan all 65535 ports
3. Perform comprehensive web testing
4. Enumerate DNS
5. Apply AI/ML analysis
6. Generate professional reports
"""

# Python API Usage
"""
from src.scanner import NetworkScanner, WebScanner, DNSScanner
from src.ai_engine import ThreatAnalyzer
from src.reporting import ReportGenerator
from src.utils.logger import color_logger

# Network Scanning
scanner = NetworkScanner(threads=4)
hosts = scanner.ping_sweep("192.168.1.0/24")

for host in hosts:
    host_info = scanner.scan_ports(host, ports="1-1000")
    print(f"Found {len(host_info.open_ports)} open ports on {host}")

# Web Scanning
web_scanner = WebScanner()
vulnerabilities = web_scanner.scan_url("https://example.com", crawl=True, depth=2)

for vuln in vulnerabilities:
    print(f"Found: {vuln.name} - {vuln.severity}")

# DNS Enumeration
dns_scanner = DNSScanner()
records = dns_scanner.enumerate_dns_records("example.com")
subdomains = dns_scanner.find_subdomains_dns("example.com")

# AI Analysis
analyzer = ThreatAnalyzer()
findings = {
    'vulnerabilities': [v.__dict__ for v in vulnerabilities],
    'target': 'example.com'
}
analysis = analyzer.analyze_findings(findings)

# Report Generation
reporter = ReportGenerator(output_dir="reports")
reporter.generate_html_report(findings)
reporter.generate_json_report(findings)

color_logger.success("Assessment complete!", "COMPLETE")
"""

# Configuration Examples

# Example: Custom Configuration
"""
# Save to config/xbow.json:
{
  "scan": {
    "timeout": 60,
    "threads": 8,
    "log_level": "DEBUG"
  },
  "network": {
    "port_range": "1-65535",
    "enable_os_detection": true
  },
  "web": {
    "crawl_depth": 4,
    "follow_redirects": true
  },
  "ai": {
    "enable_ml": true,
    "confidence_threshold": 0.8
  }
}

Then run with: xbow scan --config config/xbow.json --target target.com
"""

# Advanced Techniques

# 1. Targeted Port Scanning
"""
# Scan only web services
xbow scan --target 192.168.1.100 --ports 80,443,8080,8443,8888

# Scan specific service ports
xbow scan --target 192.168.1.100 --ports 22,23,3306,5432,27017
"""

# 2. Large-Scale Scanning
"""
# Scan entire subnet for quick reconnaissance
xbow scan --target 10.0.0.0/8 --scan-type network --profile quick

# Deep web application testing
xbow scan --target https://example.com --scan-type web --depth 5 --threads 4
"""

# 3. Subdomain Enumeration for Security Research
"""
xbow enumerate --target example.com

# This will find all subdomains and their DNS records, useful for:
# - Identifying exposed services
# - Finding staging/dev environments
# - Discovering misconfigured systems
"""

# 4. Chain Multiple Scans
"""
# First: Network reconnaissance
xbow scan --target 192.168.1.0/24 --scan-type network --output results/network

# Second: Web scan on discovered services
xbow scan --target https://webserver.internal --scan-type web --output results/web

# Third: DNS enumeration
xbow enumerate --target example.internal --output results/dns
"""

# Output and Reporting

# Generated Files:
"""
results/
├── pentest_report_20240128_120000.html    # Interactive HTML report
├── pentest_report_20240128_120000.json    # Machine-readable results
├── subdomains.json                         # DNS enumeration results
└── xbow_20240128_120000.log               # Detailed log file

The HTML report includes:
- Executive summary
- Risk ratings and statistics
- Detailed vulnerability information
- Remediation recommendations
- Professional formatting for client delivery
"""

# Best Practices

"""
1. Obtain Written Authorization
   - Always get explicit permission before testing
   - Document scope and timeline
   - Have rules of engagement in place

2. Start with Reconnaissance
   - Perform DNS enumeration first
   - Identify target scope
   - Map network architecture

3. Escalate Gradually
   - Start with quick scan
   - Then standard scan
   - Use aggressive only if needed

4. Validate Findings
   - Manually verify critical vulnerabilities
   - Avoid false positives
   - Document evidence

5. Secure Reporting
   - Use encrypted transport for reports
   - Mark as confidential
   - Deliver securely to authorized personnel

6. Follow-up Testing
   - Re-scan after remediations
   - Verify patches are effective
   - Document improvement
"""

# Troubleshooting Tips

"""
1. "nmap not found" Error:
   apt-get install nmap  # Linux
   brew install nmap     # macOS

2. "Connection refused" on Web Scans:
   - Verify URL is correct
   - Check network connectivity
   - Try with --verify-ssl false

3. "Timeout" Errors:
   - Increase timeout: update config.json
   - Reduce number of threads
   - Check network latency

4. Slow Scanning:
   - Reduce port range
   - Use quick profile
   - Increase number of threads

5. SSL Certificate Errors:
   - Use HTTP instead of HTTPS
   - Set verify_ssl: false in config
   - Install CA certificate
"""

# Performance Metrics

"""
Expected scanning times (approximate):

Quick scan (100 ports, single host):
  - Network only: 10-30 seconds
  - With OS detection: 30-60 seconds

Standard scan (1000 ports, single host):
  - Network only: 2-5 minutes
  - With OS detection: 5-10 minutes

Web scan (single domain):
  - Shallow (depth 1): 1-2 minutes
  - Standard (depth 2): 2-5 minutes
  - Deep (depth 3+): 5-15 minutes

Full pentest (domain + network):
  - Quick mode: 5-10 minutes
  - Standard mode: 15-30 minutes
  - Aggressive mode: 30+ minutes
"""

# Security Considerations

"""
⚠️ CRITICAL NOTES:

1. Legal Compliance
   - Penetration testing without authorization is illegal
   - Violators can face criminal charges
   - Always obtain written permission

2. Data Protection
   - Scan results may contain sensitive data
   - Encrypt reports in transit
   - Securely delete after use
   - Follow GDPR/regulatory requirements

3. System Impact
   - Aggressive scanning can impact production systems
   - Coordinate with system administrators
   - Schedule scans during maintenance windows
   - Monitor system performance during scans

4. Responsible Disclosure
   - Report vulnerabilities responsibly
   - Give vendors time to patch
   - Follow responsible disclosure timelines
   - Coordinate with security teams

5. Tool Limitations
   - XBOW is a tool, not a silver bullet
   - Manual testing still required
   - Professional judgment essential
   - Complement with other tools
"""
