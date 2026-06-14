"""
Documentation - Getting Started with XBOW
"""

# XBOW - AI Penetration Testing Framework

## Quick Start Guide

### Installation

```bash
# Clone repository
cd /path/to/XBOW

# Install dependencies
pip install -r requirements.txt

# Install XBOW
python -m pip install -e .
```

### Basic Usage

```bash
# Display help
xbow --help

# Quick network scan
xbow scan --target 192.168.1.0/24 --scan-type network

# Web application scan
xbow scan --target https://example.com --scan-type web --generate-report

# DNS enumeration
xbow enumerate --target example.com

# Full penetration test
xbow scan --target example.com --scan-type full --profile aggressive --generate-report
```

## Commands

### scan
Perform security scanning on targets

Options:
- `--target, -t`: Target (IP, CIDR, domain, or URL)
- `--scan-type, -s`: Type of scan (network, web, dns, full)
- `--ports, -p`: Port range (default: 1-1000)
- `--depth, -d`: Web crawl depth (default: 2)
- `--threads`: Number of threads (default: 4)
- `--output, -o`: Output directory
- `--generate-report`: Generate HTML and JSON reports

### enumerate
Perform DNS enumeration and subdomain discovery

Options:
- `--target, -t`: Target domain
- `--wordlist, -w`: Wordlist file
- `--output, -o`: Output file

### config
Display current configuration

## Scan Types

### Network Scan
- Host discovery via ping sweep
- Port scanning (TCP/UDP)
- Service detection
- OS detection
- Vulnerability assessment

### Web Scan
- Security header analysis
- Common path discovery
- Injection point testing
- SSL/TLS certificate verification
- Cache header analysis
- Website crawling

### DNS Scan
- DNS record enumeration (A, AAAA, MX, NS, TXT, etc.)
- Subdomain discovery
- Zone transfer attempts
- Reverse DNS lookup
- DNSSEC validation

## AI/ML Features

XBOW includes intelligent vulnerability analysis:

- **Severity Classification**: Machine learning-based severity prediction
- **Vulnerability Prediction**: Predicts related vulnerabilities
- **Impact Assessment**: Analyzes confidentiality, integrity, availability impact
- **Risk Rating**: Overall risk assessment

## Report Generation

XBOW generates professional reports in multiple formats:

- **HTML Report**: Full-featured interactive report with findings
- **JSON Report**: Machine-readable structured data

Reports include:
- Executive summary
- Vulnerability details with remediation
- Risk ratings and severity levels
- Recommendations

## Configuration

Edit `config/xbow.json` to customize:

- Scan timeout and retries
- Thread count
- SSL verification
- Log level
- Output directory

## Security Considerations

⚠️ **IMPORTANT**: 
- Only use XBOW on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- Always obtain written authorization before penetration testing
- Use this tool responsibly and ethically

## Troubleshooting

### nmap not found
Install nmap: `apt-get install nmap` (Linux) or `brew install nmap` (macOS)

### DNS resolution fails
Check network connectivity and DNS server configuration

### SSL verification errors
Use `--verify-ssl false` flag or configure custom CA certificates

## Architecture

```
XBOW Framework
├── CLI Layer (Click)
├── Scanning Layer (Network, Web, DNS)
├── Analysis Layer (Vulnerability DB)
├── AI Layer (ML Classification)
├── Exploitation Layer (Optional)
└── Reporting Layer (HTML, JSON)
```

## Advanced Features

### Custom Scan Profiles
Define custom scan profiles in `config/profiles.json`

### Vulnerability Database
Update CVE database in `config/cve_database.json`

### API Integration
XBOW can be imported as a module:

```python
from src.scanner import NetworkScanner
from src.ai_engine import ThreatAnalyzer

scanner = NetworkScanner()
hosts = scanner.ping_sweep("192.168.1.0/24")

analyzer = ThreatAnalyzer()
analysis = analyzer.analyze_findings(findings)
```

## Performance Tips

1. Use appropriate thread count based on system resources
2. Limit port range for faster scans
3. Use quick profile for initial reconnaissance
4. Reduce crawl depth for web scans
5. Run concurrent scans on multiple systems

## Support & Documentation

For detailed documentation, see:
- README.md - Project overview
- This file - Getting started guide
- Code comments - Implementation details

## Contributing

To extend XBOW:
1. Add new scanner modules in `src/scanner/`
2. Extend AI analysis in `src/ai_engine/`
3. Add new report formats in `src/reporting/`
4. Update CLI in `src/cli.py`

## License

Proprietary - XBOW Framework
