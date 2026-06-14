# XBOW AI Penetration Testing Tool

A professional-grade, AI-powered penetration testing framework with advanced vulnerability detection, automated scanning, and intelligent reporting.

## Features

- **Network Scanning**: Advanced host discovery and port scanning
- **Web Vulnerability Scanning**: Web application security testing
- **DNS Enumeration**: Subdomain discovery and DNS reconnaissance
- **Live Penetration Testing**: Interactive shell and real-time monitoring
- **Comprehensive Pentesting**: Full penetration testing workflows
- **Vulnerability Database**: Integrated CVE and known vulnerability detection
- **AI/ML Analysis**: Machine learning-based vulnerability classification and severity prediction
- **Report Generation**: Professional HTML and PDF reports
- **Multi-Protocol Support**: TCP, UDP, HTTP/HTTPS, DNS
- **Automated Exploitation Framework**: Basic exploitation for confirmed vulnerabilities
- **Real-time Logging**: Comprehensive audit trails and logging
- **Configuration Profiles**: Predefined and custom scan profiles

## Installation

```bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m xbow --help



## Quick Start

```bash
# Basic network scan
 xbow scan --target 192.168.1.0/24 --scan-type network

# Web vulnerability scan
xbow scan --target https://example.com --scan-type web

# Full penetration test
 xbow pentest --target example.com --profile aggressive --generate-report

# Live interactive pentesting
 xbow live --target https://example.com --mode interactive

# Real-time monitoring
xbow live --target https://example.com --mode monitor --duration 600

# AI automated pentesting
xbow live --target https://example.com --mode auto --duration 300
xbow live --target https://example.com --mode auto --enable-ai-agent --duration 300

# DNS enumeration
xbow enumerate --target example.com
```

## Live Interactive Pentesting

XBOW features a powerful interactive shell for real-time penetration testing:

### Interactive Commands

```bash
# Start interactive session
xbow live --target https://example.com --mode interactive

# Available commands:
scan web          # Scan for web vulnerabilities
list              # List found vulnerabilities with IDs
exploit 1         # Attempt exploitation of vulnerability ID 1
nmap -p 80,443    # Run nmap scan
sqlmap -u URL     # Run sqlmap injection test
info              # Show target information
help              # Show help
quit              # Exit session
```

### Interactive Exploitation Features

- **Session Persistence**: Vulnerabilities discovered during the session are tracked with unique IDs
- **Safe Exploitation**: All exploitation attempts use safe mode to avoid actual damage
- **Multi-Tool Integration**: Direct access to nmap, sqlmap, nikto, dirb, and metasploit
- **Real-time Results**: Immediate feedback on scan and exploitation results

### AI Automated Mode

The AI automated mode uses intelligent decision-making to perform comprehensive pentesting:

```bash
# AI-driven automated pentesting
xbow live --target https://example.com --mode auto --duration 300
```

**AI Features:**
- **Intelligent Scanning**: Automatically chooses scan types based on findings
- **Adaptive Exploitation**: Attempts exploitation of high-severity vulnerabilities
- **Tool Integration**: Automatically runs nmap, sqlmap, and other tools when appropriate
- **Decision Making**: AI analyzes results and decides next actions
- **AI Agent Plugins**: External AI orchestration providers can be configured in `config/ai_agents.json`
- **Comprehensive Reporting**: Generates detailed summary of all automated actions

## Project Structure

```
xbow/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── scanner/               # Core scanning modules
│   │   ├── network.py
│   │   ├── web.py
│   │   ├── dns.py
│   │   └── vulnerability.py
│   ├── ai_engine/             # ML/AI analysis
│   │   ├── classifier.py
│   │   ├── predictor.py
│   │   └── models/
│   ├── exploits/              # Exploitation framework
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── payloads/
│   ├── reporting/             # Report generation
│   │   ├── html_report.py
│   │   ├── pdf_report.py
│   │   └── templates/
│   ├── utils/                 # Utility functions
│   │   ├── logger.py
│   │   ├── config.py
│   │   └── helpers.py
│   └── database/              # Vulnerability DB
├── config/                    # Configuration files
│   ├── xbow.cfg
│   ├── profiles.json
│   └── cve_database.json
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── requirements.txt
├── setup.py
└── LICENSE
```

## Architecture

XBOW uses a modular architecture:

1. **CLI Layer**: User interface and command handling
2. **Scanning Layer**: Parallel scanning engines
3. **Analysis Layer**: Data processing and correlation
4. **AI Layer**: ML-based vulnerability classification
5. **Exploitation Layer**: Safe exploitation testing
6. **Reporting Layer**: Multi-format report generation

## Security Considerations

⚠️ **Legal Notice**: This tool is for authorized security testing only. Unauthorized access to computer systems is illegal. Always obtain written permission before conducting penetration tests.

## Dependencies

- Python 3.9+
- Network tools (nmap, masscan)
- Machine Learning libraries (scikit-learn, TensorFlow)
- Web scraping (Selenium, requests)
- Report generation (Jinja2, WeasyPrint)

## Documentation

See [docs/](docs/) for comprehensive documentation and examples.

## License

Proprietary - XBOW Framework

## Author

Advanced Penetration Testing Team
