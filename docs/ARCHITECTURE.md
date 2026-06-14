"""
ARCHITECTURE.md - XBOW Framework Design and Architecture
"""

# XBOW Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface (CLI)                  │
│                     (Click Framework)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────────────────┐
│                   Orchestration Layer                         │
│  (Scan coordination, task management, progress tracking)     │
└────┬──────────────┬──────────────────┬──────────────────────┘
     │              │                  │
     ▼              ▼                  ▼
┌──────────┐  ┌──────────┐  ┌──────────────────┐
│ Network  │  │   Web    │  │      DNS         │
│ Scanner  │  │ Scanner  │  │   Scanner        │
│          │  │          │  │                  │
│- Ping    │  │- Headers │  │- Zone Transfer   │
│- Ports   │  │- Paths   │  │- Records         │
│- Services   │- Injection   │- Subdomains     │
└──────────┘  │- SSL     │  │- Reverse DNS     │
              │- Crawl   │  │- DNSSEC          │
              └──────────┘  └──────────────────┘
                     │              │
                     └──────┬───────┘
                            │
        ┌───────────────────▼──────────────────┐
        │  Vulnerability Detection & Analysis   │
        │  - Pattern matching                  │
        │  - Database lookup                   │
        │  - CVE correlation                   │
        └───────────────────┬──────────────────┘
                            │
        ┌───────────────────▼──────────────────┐
        │      AI/ML Analysis Engine            │
        │  - Classifier                        │
        │  - Predictor                         │
        │  - Threat Analyzer                   │
        └───────────────────┬──────────────────┘
                            │
        ┌───────────────────▼──────────────────┐
        │    Report Generation Engine           │
        │  - HTML Reports                      │
        │  - JSON Export                       │
        │  - Remediation Templates             │
        └─────────────────────────────────────┘
```

## Module Breakdown

### 1. Scanner Module (`src/scanner/`)

**Components:**

#### `network.py` - Network Scanning
- **NetworkScanner Class**
  - `ping_sweep()`: Host discovery
  - `scan_ports()`: Port enumeration
  - `service_detection()`: Service identification
  - `os_detection()`: Operating system fingerprinting
  
- **Features**
  - Dual implementation (with/without nmap)
  - Multi-threaded scanning
  - Configurable timeouts and retries

#### `web.py` - Web Application Scanning
- **WebScanner Class**
  - `scan_url()`: Full web assessment
  - `_scan_headers()`: Security header analysis
  - `_scan_common_paths()`: Sensitive path discovery
  - `_scan_injection_points()`: Vulnerability testing
  - `_crawl_site()`: Website enumeration
  - `check_ssl_certificate()`: SSL/TLS validation
  - `check_caching_headers()`: Cache security

- **Features**
  - SSL/TLS analysis
  - Common vulnerability testing
  - Website crawling
  - Request/response analysis

#### `dns.py` - DNS Enumeration
- **DNSScanner Class**
  - `get_dns_records()`: DNS record queries
  - `enumerate_dns_records()`: Full enumeration
  - `find_subdomains_dns()`: Subdomain discovery
  - `zone_transfer()`: Zone transfer attempts
  - `reverse_dns_lookup()`: Reverse resolution
  - `check_dns_security()`: DNSSEC validation

- **Features**
  - Support for multiple record types (A, AAAA, MX, NS, TXT, etc.)
  - Subdomain wordlist enumeration
  - Zone transfer detection

#### `vulnerability.py` - Vulnerability Detection
- **VulnerabilityDatabase Class**
  - CVE database management
  - Local vulnerability lookup

- **VulnerabilityDetector Class**
  - Service vulnerability matching
  - Default credential suggestions
  - Weak cipher detection
  - Exploitation difficulty assessment

### 2. AI/ML Engine (`src/ai_engine/`)

#### `classifier.py` - Intelligent Classification
- **VulnerabilityClassifier**
  - Machine learning-based severity prediction
  - Rule-based classification fallback
  - Feature extraction
  - Confidence scoring

- **VulnerabilityPredictor**
  - Predicts related vulnerabilities
  - Analyzes vulnerability chains
  - Impact assessment

- **ThreatAnalyzer**
  - Comprehensive findings analysis
  - Risk rating calculation
  - Automated threat intelligence

### 3. Reporting Module (`src/reporting/`)

#### `html_report.py` - Report Generation
- **ReportGenerator Class**
  - HTML report generation
  - JSON report export
  - Professional formatting
  - Remediation recommendations

### 4. Utilities (`src/utils/`)

#### `logger.py` - Logging and Output
- Structured logging with loguru
- Colored console output
- File logging with rotation
- Audit trail generation

#### `config.py` - Configuration Management
- Multi-section configuration
- Scan profiles
- Persistent settings
- Runtime configuration

#### `helpers.py` - Utility Functions
- IP/CIDR validation
- Port range parsing
- Command execution
- Risk level constants

### 5. CLI Module (`src/cli.py`)

**Commands:**
- `scan`: Execute security scans
- `enumerate`: DNS enumeration
- `config`: Configuration display

**Features:**
- Click-based CLI
- Flexible argument parsing
- Progress indication
- Result formatting

## Data Flow

```
User Input (CLI)
       │
       ▼
Config Manager (Load settings)
       │
       ▼
Scanner Selection (Network/Web/DNS)
       │
       ├─▶ Network Scanner ──┐
       ├─▶ Web Scanner ──────┼──▶ Raw Findings
       └─▶ DNS Scanner ──────┘
                               │
                               ▼
                    Vulnerability Detector
                               │
                               ▼
                    AI/ML Analysis Engine
                               │
                               ├─▶ Classifier (Severity)
                               ├─▶ Predictor (Related vulns)
                               └─▶ Threat Analyzer (Overall risk)
                               │
                               ▼
                    Report Generator
                               │
                               ├─▶ HTML Report
                               └─▶ JSON Export
                               │
                               ▼
                          Output Files
```

## Class Hierarchies

### Scanner Hierarchy
```
BaseScanner (conceptual)
├── NetworkScanner
│   ├── HostInfo
│   └── PortInfo
├── WebScanner
│   └── Vulnerability
├── DNSScanner
│   └── DNSRecord
└── VulnerabilityDetector
```

### Data Models
```
Vulnerability
├── name (str)
├── type (str)
├── url (str)
├── severity (str: CRITICAL|HIGH|MEDIUM|LOW|INFO)
├── description (str)
├── remediation (str)
└── evidence (str)

HostInfo
├── ip (str)
├── hostname (Optional[str])
├── open_ports (List[PortInfo])
├── os_info (Optional[str])
└── services (Dict)

PortInfo
├── port (int)
├── protocol (str)
├── state (str: open|closed|filtered)
├── service (Optional[str])
└── version (Optional[str])
```

## Scanning Workflow

### 1. Network Scan Flow
```
Validate Target
    ↓
Expand CIDR (if applicable)
    ↓
Ping Sweep (Host Discovery)
    ↓
For Each Live Host:
    ├─ Port Scan
    ├─ Service Detection
    └─ OS Detection
    ↓
Vulnerability Assessment
    ↓
Results
```

### 2. Web Scan Flow
```
Validate URL
    ↓
Security Headers Analysis
    ↓
Common Paths Scan
    ↓
Injection Testing
    ↓
Website Crawling (Depth-based)
    ↓
SSL/TLS Validation
    ↓
Cache Security Check
    ↓
Results
```

### 3. DNS Scan Flow
```
Validate Domain
    ↓
Enumerate Record Types
    ├─ A, AAAA, MX, NS, TXT, etc.
    ↓
Subdomain Discovery
    ├─ Wordlist-based
    ├─ Zone Transfer Attempt
    ↓
Reverse DNS Lookups
    ↓
DNSSEC Validation
    ↓
Results
```

## Performance Considerations

### Concurrency
- Multi-threaded port scanning
- Configurable thread pool size
- Queue-based task distribution

### Optimization
- Early exit on timeout
- Retry logic for failed requests
- Connection pooling for HTTP
- DNS caching

### Resource Management
- Memory-efficient streaming
- Process pooling for heavy operations
- Proper cleanup and resource release

## Security Architecture

### Input Validation
- URL/IP validation
- CIDR notation validation
- Port range validation
- Domain name validation

### Safe Execution
- Command injection prevention
- Timeout controls
- Exception handling
- Resource limits

### Data Protection
- No credential storage
- Secure logging
- Output sanitization
- Report encryption support

## Extension Points

### Adding New Scanners
1. Create new scanner class in `src/scanner/`
2. Implement common interface
3. Register in CLI module
4. Add tests in `tests/`

### Custom Vulnerabilities
1. Extend `VulnerabilityDetector`
2. Add patterns to `vulnerable_patterns`
3. Update vulnerability database

### Report Formats
1. Create new format class in `src/reporting/`
2. Inherit from `ReportGenerator`
3. Implement format-specific logic
4. Register in CLI

### AI Models
1. Train custom ML models
2. Save to `models/` directory
3. Update classifier paths
4. Test with sample data

## Technology Stack

- **Language**: Python 3.9+
- **CLI**: Click
- **Logging**: Loguru
- **ML/AI**: scikit-learn, TensorFlow, joblib
- **Network**: nmap, python-nmap, scapy
- **Web**: requests, BeautifulSoup4, Selenium
- **DNS**: dnspython
- **Reporting**: Jinja2, WeasyPrint
- **Testing**: pytest

## Future Enhancements

1. **Advanced AI**
   - Deep learning models
   - Anomaly detection
   - Behavioral analysis

2. **Exploitation**
   - Automated exploitation
   - Payload generation
   - Metasploit integration

3. **Collaboration**
   - Team collaboration features
   - Result sharing
   - Real-time scanning dashboard

4. **Integration**
   - SIEM integration
   - Ticketing system integration
   - Webhook support

5. **Performance**
   - GPU acceleration
   - Distributed scanning
   - Cloud support
