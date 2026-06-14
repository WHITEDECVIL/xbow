"""
PROJECT_STRUCTURE.md - Complete XBOW Project Layout
"""

# XBOW Project Structure

```
XBOW/
├── README.md                    # Project overview and features
├── LICENSE                      # Proprietary license
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation configuration
├── Makefile                     # Development commands
├── .gitignore                   # Git ignore patterns
├── install.sh                   # Automated installation script
│
├── src/                         # Main source code
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Command-line interface (main entry point)
│   │
│   ├── scanner/                # Scanning modules
│   │   ├── __init__.py
│   │   ├── network.py          # Network scanner (ping sweep, port scan)
│   │   ├── web.py             # Web application scanner
│   │   ├── dns.py             # DNS enumeration scanner
│   │   └── vulnerability.py    # Vulnerability detection and database
│   │
│   ├── ai_engine/              # AI/ML Analysis
│   │   ├── __init__.py
│   │   └── classifier.py       # ML classification, prediction, threat analysis
│   │
│   ├── reporting/              # Report generation
│   │   ├── __init__.py
│   │   ├── html_report.py      # HTML and JSON report generation
│   │   └── templates/          # Report templates (future)
│   │
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── logger.py           # Structured logging and colored output
│       ├── config.py           # Configuration management
│       └── helpers.py          # Helper functions and constants
│
├── config/                      # Configuration and data files
│   ├── xbow.json               # Main configuration (scan settings, timeouts)
│   ├── profiles.json           # Scan profiles (quick, standard, aggressive)
│   ├── cve_database.json       # CVE database (local copy)
│   └── wordlists/              # Subdomain/path wordlists (optional)
│
├── models/                      # Machine learning models
│   ├── vulnerability_classifier.pkl  # Pre-trained classifier (optional)
│   └── README.md               # Model documentation
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_helpers.py         # Tests for utility functions
│   ├── test_scanners.py        # Tests for scanners (future)
│   └── test_ai_engine.py       # Tests for AI/ML (future)
│
├── docs/                        # Documentation
│   ├── README.md               # Documentation index
│   ├── GETTING_STARTED.md      # Quick start guide
│   ├── EXAMPLES.md             # Usage examples and scenarios
│   ├── ARCHITECTURE.md         # System design and architecture
│   ├── API.md                  # Python API documentation (future)
│   └── TROUBLESHOOTING.md      # Common issues and solutions (future)
│
├── results/                     # Output directory (generated)
│   ├── pentest_report_*.html   # Generated HTML reports
│   ├── pentest_report_*.json   # Generated JSON reports
│   └── subdomains.json         # DNS enumeration results
│
├── logs/                        # Log files (generated)
│   ├── xbow_*.log              # Detailed execution logs
│   └── README.md               # Log file documentation
│
└── .github/                     # GitHub configuration (future)
    ├── workflows/              # CI/CD workflows
    ├── ISSUE_TEMPLATE.md       # Issue template
    └── PULL_REQUEST_TEMPLATE.md # PR template
```

## File Descriptions

### Core Files

**README.md** (65 lines)
- Project overview
- Features list
- Installation instructions
- Quick start examples
- Architecture overview
- Security notices

**setup.py** (35 lines)
- Package metadata
- Dependency specification
- Entry point configuration
- Distribution settings

**requirements.txt** (55 lines)
- Core framework dependencies
- Network/scanning tools
- ML/AI libraries
- Web scraping tools
- Report generation tools
- Testing and development tools

### Source Code (`src/`)

**cli.py** (485 lines)
- Main CLI interface
- Commands: scan, enumerate, config
- Output formatting
- Result display
- Report generation integration

**scanner/network.py** (380 lines)
- NetworkScanner class
- Ping sweep implementation
- Port scanning (nmap and manual)
- Service detection
- OS detection
- HostInfo and PortInfo dataclasses

**scanner/web.py** (340 lines)
- WebScanner class
- Security header analysis
- Common path scanning
- Injection point testing
- Website crawling
- SSL/TLS validation
- Cache header analysis
- Vulnerability dataclass

**scanner/dns.py** (285 lines)
- DNSScanner class
- DNS record enumeration
- Subdomain discovery
- Zone transfer attempts
- Reverse DNS lookup
- DNSSEC validation
- DNSRecord dataclass

**scanner/vulnerability.py** (215 lines)
- VulnerabilityDatabase class
- VulnerabilityDetector class
- CVE database management
- Service vulnerability matching
- Default credential suggestions
- Cipher strength assessment

**ai_engine/classifier.py** (380 lines)
- VulnerabilityClassifier (ML + rule-based)
- VulnerabilityPredictor
- ThreatAnalyzer
- Feature extraction
- Severity classification
- Impact assessment

**reporting/html_report.py** (320 lines)
- ReportGenerator class
- HTML report generation with styling
- JSON report export
- Recommendation generation
- Professional formatting

**utils/logger.py** (110 lines)
- Structured logging setup
- Colored console output
- File logging with rotation
- ColorLogger class

**utils/config.py** (175 lines)
- ConfigManager class
- Configuration dataclasses
- Config loading/saving
- Profile management

**utils/helpers.py** (165 lines)
- IP/CIDR validation and expansion
- Domain validation
- Port parsing
- Command execution
- Risk level constants
- Color code definitions

### Configuration (`config/`)

**xbow.json** (25 lines)
- Scan timeout and retries
- Thread configuration
- Log level
- Network settings
- Web settings
- AI settings

**profiles.json** (30 lines)
- Quick profile: 100 ports, minimal testing
- Standard profile: 1000 ports, full testing
- Aggressive profile: all ports, deep testing
- Web-only profile: focused web testing
- Network-only profile: reconnaissance only

**cve_database.json** (25 lines)
- Sample CVE entries
- Vulnerability descriptions
- Severity ratings
- Affected software list

### Documentation (`docs/`)

**GETTING_STARTED.md** (240 lines)
- Installation instructions
- Quick start guide
- Command reference
- Scan type explanations
- Configuration guide
- Troubleshooting tips

**EXAMPLES.md** (360 lines)
- Basic usage examples
- Python API usage
- Configuration examples
- Advanced techniques
- Output descriptions
- Best practices
- Performance metrics
- Security considerations

**ARCHITECTURE.md** (520 lines)
- System architecture diagram
- Module breakdown
- Data flow description
- Class hierarchies
- Scanning workflows
- Performance considerations
- Security architecture
- Extension points
- Technology stack
- Future enhancements

### Tests (`tests/`)

**test_helpers.py** (50 lines)
- Tests for IP validation
- Tests for CIDR validation
- Tests for port parsing
- Tests for risk levels

## Statistics

- **Total Files**: 28
- **Total Lines of Code**: ~4,500
- **Python Files**: 18
- **Documentation Files**: 8
- **Config Files**: 3
- **Scripts**: 1

## Key Features by File

### Network Scanning
- `scanner/network.py`: Ping sweep, port scanning, service detection, OS detection

### Web Scanning
- `scanner/web.py`: Header analysis, injection testing, crawling, SSL validation

### DNS Enumeration
- `scanner/dns.py`: Record enumeration, subdomain discovery, zone transfer, DNSSEC

### Vulnerability Detection
- `scanner/vulnerability.py`: CVE lookup, service matching, credential suggestions

### AI/ML Analysis
- `ai_engine/classifier.py`: Severity prediction, vulnerability correlation, threat analysis

### Reporting
- `reporting/html_report.py`: Professional HTML reports, JSON export, recommendations

### CLI Interface
- `cli.py`: User-friendly command interface with multiple scan types

### Utilities
- `utils/logger.py`: Colored logging and structured output
- `utils/config.py`: Configuration management with profiles
- `utils/helpers.py`: Validation and helper functions

## Dependencies by Category

**Network Tools**: nmap, scapy, python-nmap, requests
**ML/AI**: scikit-learn, numpy, pandas, tensorflow, joblib
**Web Tools**: selenium, beautifulsoup4, requests, lxml
**DNS**: dnspython
**Reporting**: jinja2, weasyprint
**Utilities**: click, loguru, colorama, rich, pydantic
**Testing**: pytest, pytest-asyncio

## Entry Points

**CLI Entry Point**:
- Command: `xbow`
- Module: `src.cli:main`
- Handler: Click CLI application

**Python API Entry Point**:
- Import: `from src.scanner import NetworkScanner`
- Usage: Direct class instantiation

## Build and Deploy

**Installation**:
```bash
bash install.sh          # Automatic setup
# or
pip install -r requirements.txt
pip install -e .
```

**Running**:
```bash
xbow --help             # CLI help
xbow scan --target ...  # Execute scan
python -m src.cli       # Direct module execution
```

**Development**:
```bash
make install-dev        # Install with dev dependencies
make test              # Run tests
make lint              # Check code quality
make format            # Format code
```

## Version Control

**.gitignore** includes:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Build artifacts (`build/`, `dist/`, `*.egg-info`)
- Test coverage (`.pytest_cache/`, `.coverage`)
- Reports and results (`.json`, `.html`)
- System files (`.DS_Store`, `Thumbs.db`)

## Documentation Coverage

- **Installation**: README.md, GETTING_STARTED.md, install.sh
- **Usage**: GETTING_STARTED.md, EXAMPLES.md, cli.py docstrings
- **Architecture**: ARCHITECTURE.md, code comments
- **API**: Docstrings in all modules
- **Configuration**: config files with comments
- **Testing**: test files with examples
