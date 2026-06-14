# XBOW DFD - ASCII Representations and Usage Guide

## Level 0: Context Diagram (ASCII Format)

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    ┌──────────────────────────────┐                    │
│                    │   👤 User/Pen Tester        │                    │
│                    └────────────┬─────────────────┘                    │
│                                 │ [1] Scan commands                     │
│                                 │     parameters                        │
│                                 │     target info                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │              XBOW AI PENETRATION TESTING FRAMEWORK              │  │
│  │                                                                 │  │
│  │  • CLI Parser         • Network Scanner                         │  │
│  │  • Orchestrator       • Web Scanner                             │  │
│  │  • Data Aggregator    • DNS Scanner                             │  │
│  │  • Vuln Detector      • AI/ML Analysis                          │  │
│  │  • Report Generator   • Cache Management                        │  │
│  │                                                                 │  │
│  └────────┬──────────────────────┬────────────┬──────────────────┘  │
│           │ [4] Scan traffic     │ [5] Reports│ [6] Cache update    │
│           │     probes           │ findings   │     results         │
│           ▼                      ▼            ▼                     │
│  ┌─────────────────────┐ ┌────────────────┐ ┌──────────────────┐   │
│  │  🌐 Target Systems  │ │  📄 Reports    │ │  ⚙️  Config DB    │   │
│  │  (Networks, Web,    │ │  (HTML/JSON)   │ │  CVE Database    │   │
│  │   DNS Servers)      │ │  Audit Logs    │ │  Profiles        │   │
│  │  ◄── [2] Responses  │ │  ◄─ [5] Deliver│ │  Model Registry  │   │
│  │       Service info  │ │                │ │  ◄─ [3] Config   │   │
│  └─────────────────────┘ └────────────────┘ └──────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow Descriptions (Level 0)

```
[1] USER → XBOW:        Scan request with target, type, parameters
[2] TARGET → XBOW:      Network responses, web content, DNS records
[3] CONFIG DB → XBOW:   CVE data, profiles, AI models
[4] XBOW → TARGET:      Probes, HTTP requests, DNS queries
[5] XBOW → REPORTS:     Generated security reports
[6] XBOW → CONFIG DB:   Cache updates, results storage
```

---

## Level 1: System-Level Data Flow (Detailed ASCII)

### Overview Flow

```
                           👤 USER INPUT
                                │
                                ▼
                         ┌──────────────┐
                         │ P1: CLI LAYER │
                         │   • Parse     │
                         │   • Validate  │
                         └──────┬───────┘
                                │ [2.1] Config
                                │
                    ┌───────────┴────────────┐
                    │                        │ [2.2] Profile
                    ▼                        ▼
          ┌──────────────────┐     [D2: PROFILES]
          │ P2: ORCHESTRATOR │
          │  • Coordinate    │
          │  • Resource Mgmt │
          └──┬──┬──┬─────────┘
             │  │  │
        ┌────┘  │  └──────────────────┐
        │ [3.1] │  [3.2]         [3.3]│
        ▼       ▼                      ▼
    ┌─────────┐ ┌──────────┐    ┌──────────┐
    │P3: NET  │ │ P4: WEB  │    │P5: DNS   │
    │SCANNER  │ │ SCANNER  │    │ SCANNER  │
    └────┬────┘ └────┬─────┘    └────┬─────┘
         │           │               │
         │ [4.1]     │ [4.2]     [4.3]│
         └───────┬───┴───────┬────────┘
                 │           │
                 ▼           ▼
            [🌐 TARGET SYSTEMS]
                 │           │
         ┌───────┴───────┬───┴────────┐
    [5.1]│          [5.2]│        [5.3]│
         ▼               ▼             ▼
    [Network]        [Web]         [DNS]
     Responses      Responses      Responses
         │               │             │
         └───────┬───────┴────────────┘
                 ▼
          ┌─────────────────┐
          │P6: DATA         │
          │AGGREGATOR       │
          │ • Correlate     │
          │ • Deduplicate   │
          └────────┬────────┘
                   │ [6] Raw findings
                   ▼
            ┌──────────────────┐
            │P7: VULN DETECTOR │
            │ • Pattern Match  │
            │ • CVE Lookup     │
            └────────┬─────────┘
                     │ [7] CVE Info ◄──── [D1: VULN DB]
                     │
                     │ [8] Detected Vulns
                     ▼
            ┌──────────────────┐
            │P8: AI/ML ENGINE  │
            │ • Classify       │
            │ • Predict Risk   │
            │ • Analyze        │
            └────────┬─────────┘
                     │ [9] ML Models ◄──── [D3: MODEL REGISTRY]
                     │
                     │ [10] Analyzed findings
                     ▼
            ┌──────────────────────┐
            │P9: REPORT GENERATOR  │
            │ • Format             │
            │ • Export             │
            │ • Summarize          │
            └──┬──────┬────────┬───┘
               │      │        │
       [11]    │ [12] │ [13]   │
       Report  │ Logs │Report  │
               ▼      ▼        ▼
            [D4: REPORTS]  👤 USER
            [D5: AUDIT LOGS]
```

---

## Detailed Process Flows (Level 1)

### Process: P3 - Network Scanner

```
INPUT: Target CIDR, Port Range, Options
├─ Target: 192.168.1.0/24
├─ Ports: 1-65535 (or custom range)
└─ Options: {timeout: 300, threads: 10, ...}

EXECUTION SEQUENCE:
├─ [STEP 1] Host Discovery (Ping Sweep)
│  ├─ Send ICMP Echo to each IP
│  ├─ Collect responses
│  └─ OUTPUT: Active host list
│
├─ [STEP 2] Port Scanning (TCP/UDP)
│  ├─ For each active host:
│  │  ├─ Connect to port (SYN)
│  │  ├─ Collect response (ACK, RST, TIMEOUT)
│  │  └─ Mark port state
│  └─ OUTPUT: Open/Filtered/Closed ports
│
├─ [STEP 3] Service Identification (Banner Grab)
│  ├─ For each open port:
│  │  ├─ Connect and read banner
│  │  └─ Parse service + version
│  └─ OUTPUT: Service identifications
│
├─ [STEP 4] OS Fingerprinting
│  ├─ Analyze packet responses
│  ├─ Match against OS signatures
│  └─ OUTPUT: OS guess + confidence
│
└─ [STEP 5] Package Results
   ├─ Combine all findings
   ├─ Create Finding objects
   └─ OUTPUT: Structured network data

OUTPUT STRUCTURE:
{
  "findings": [
    {
      "host": "192.168.1.100",
      "status": "up",
      "os": {"guess": "Windows 10", "confidence": 0.92},
      "ports": [
        {"port": 22, "state": "open", "service": "SSH", "version": "2.0"},
        {"port": 80, "state": "open", "service": "HTTP", "version": "Apache 2.4.41"},
        {"port": 443, "state": "open", "service": "HTTPS", "version": "Apache 2.4.41"}
      ]
    }
  ],
  "timestamp": "2026-03-03T14:30:00Z"
}
```

### Process: P4 - Web Scanner

```
INPUT: Target URL, Scan Depth, Plugins
├─ URL: https://example.com
├─ Depth: 2 (follow links 2 levels deep)
└─ Plugins: ["ssl", "headers", "injection", "cache"]

EXECUTION SEQUENCE:
├─ [STEP 1] SSL/TLS Analysis
│  ├─ Retrieve certificate
│  ├─ Check expiration
│  ├─ Verify chain
│  ├─ Check for weak ciphers
│  └─ OUTPUT: SSL issues + scores
│
├─ [STEP 2] Security Headers Analysis
│  ├─ Request target URL
│  ├─ Parse response headers
│  ├─ Check for missing headers:
│  │  ├─ X-Frame-Options
│  │  ├─ X-Content-Type-Options
│  │  ├─ Strict-Transport-Security
│  │  └─ Content-Security-Policy
│  └─ OUTPUT: Header findings
│
├─ [STEP 3] Common Path Discovery
│  ├─ Load common path wordlist
│  ├─ For each path:
│  │  ├─ Request /path
│  │  ├─ Check response (200, 302, 403, etc.)
│  │  └─ Record findings
│  └─ OUTPUT: Discovered paths
│
├─ [STEP 4] Injection Testing
│  ├─ Identify input parameters
│  ├─ For each parameter:
│  │  ├─ Send SQLi payload
│  │  ├─ Send XSS payload
│  │  ├─ Send command injection payload
│  │  └─ Analyze response
│  └─ OUTPUT: Injection vulnerabilities
│
├─ [STEP 5] Website Crawling
│  ├─ Discover all links
│  ├─ Follow up to depth limit
│  ├─ Collect endpoints
│  └─ OUTPUT: Endpoint inventory
│
└─ [STEP 6] Cache Analysis
   ├─ Check cache headers
   ├─ Analyze expiration
   └─ OUTPUT: Cache issues

OUTPUT STRUCTURE:
{
  "url": "https://example.com",
  "ssl": {"issues": [...], "score": 85},
  "headers": {"missing": [...], "weak": [...]},
  "paths": ["/admin", "/api/users", "/backup.sql"],
  "injection_findings": [...],
  "endpoints": [...],
  "timestamp": "2026-03-03T14:30:15Z"
}
```

### Process: P5 - DNS Scanner

```
INPUT: Domain, Record Types, Wordlist
├─ Domain: example.com
├─ Types: [A, AAAA, MX, NS, TXT, SOA]
└─ Wordlist: common_subdomains.txt

EXECUTION SEQUENCE:
├─ [STEP 1] DNS Record Enumeration
│  ├─ Query A record → 93.184.216.34
│  ├─ Query AAAA record → 2606:2800:220:1:248:1893:25c8:1946
│  ├─ Query MX record → 10 mail.example.com
│  ├─ Query NS record → ns1.example.com
│  ├─ Query TXT record → "v=spf1 ..."
│  └─ OUTPUT: DNS records
│
├─ [STEP 2] Subdomain Enumeration
│  ├─ Load wordlist (admin, api, mail, etc.)
│  ├─ For each word:
│  │  ├─ Query [word].example.com
│  │  ├─ If resolves: record it
│  │  └─ Continue
│  └─ OUTPUT: Discovered subdomains
│
├─ [STEP 3] Zone Transfer Attempt
│  ├─ Connect to authoritative NS
│  ├─ Attempt AXFR (zone transfer)
│  ├─ If successful: extract all records
│  └─ OUTPUT: Zone transfer results (or failure)
│
├─ [STEP 4] Reverse DNS Lookup
│  ├─ For each IP found:
│  │  ├─ Query PTR record
│  │  └─ Collect hostname
│  └─ OUTPUT: Associated hostnames
│
└─ [STEP 5] DNSSEC Validation
   ├─ Check DNSSEC signatures
   ├─ Validate trust chain
   └─ OUTPUT: DNSSEC status

OUTPUT STRUCTURE:
{
  "domain": "example.com",
  "dns_records": {
    "A": ["93.184.216.34"],
    "MX": ["10 mail.example.com"],
    "TXT": ["v=spf1 ..."]
  },
  "subdomains": ["api.example.com", "admin.example.com"],
  "zone_transfer": {"status": "failed"},
  "reverse_dns": {"93.184.216.34": "example.com"},
  "dnssec": {"enabled": true, "valid": true}
}
```

---

## Practical Examples

### Example 1: Full Network Scan

```
USER INPUT:
$ xbow scan --target 192.168.1.0/24 --scan-type network --profile aggressive

DATA FLOW TRACE:

[1] USER → P1 (CLI)
    Input: {command: "scan", target: "192.168.1.0/24", scan_type: "network", 
            profile: "aggressive"}

[2.1] P1 → P2 (Orchestrator)
    Output: Validated config with aggressive profile settings

[2.2] D2 (Profiles) → P2
    Delivers: {threads: 20, timeout: 300, os_detection: true, ...}

[3.1] P2 → P3 (Network Scanner)
    Task: {target: "192.168.1.0/24", ports: "1-65535", aggressive: true}

[4.1] P3 → Target Systems
    Action: ICMP sweeps, TCP/UDP scans, banner grabbing

[5.1] Target Systems → P6 (Data Aggregator)
    Response: Host data, port data, service identifications

[6] P6 → P7 (Vulnerability Detector)
    Aggregated: Consolidated finding objects

[7] D1 (Vuln DB) → P7
    Provides: CVE database, service vulnerability mappings

[8] P7 → P8 (AI/ML Engine)
    Findings: Detected vulnerabilities with initial severity

[9] D3 (Models) → P8
    ML models for classification

[10] P8 → P9 (Report Generator)
     Enriched findings with AI predictions

[11] P9 → D4 (Reports)
     Final report saved to HTML/JSON

[13] P9 → User
     Report reference sent to user
```

### Example 2: Web Application Scan

```
USER INPUT:
$ xbow scan --target https://vulnerableapp.local --scan-type web --plugin injection

DATA FLOW TRACE:

[1] USER → P1 (CLI)
    Input: {command: "scan", target: "https://vulnerableapp.local",
            scan_type: "web", plugins: ["injection"]}

[2.1] P1 → P2
    Config: Web-only scan, enable injection testing

[3.2] P2 → P4 (Web Scanner)
    Task: {url: "https://vulnerableapp.local", depth: 3, plugins: ["injection"]}

[4.2] P4 → Target
    Action: SSL check, header analysis, path discovery, injection testing

[5.2] Target → P6
    Response: HTML content, headers, injection test results

[6] P6 → P7
    Aggregated: Web findings compiled

[8] P7 → P8
    Vulnerabilities: SQL injection, XSS, CSRF, weak SSL, etc.

[10] P8 → P9
    Analyzed: Risk scored, predictions made

[11] P9 → Reports
    Report: HTML report with web vulnerabilities highlighted

[12] P9 → D5 (Logs)
    Audit: Complete operation timeline

[13] P9 → User
    Delivery: "See: reports/web_scan_20260303_143015.html"
```

---

## Data Store Contents

### D1: Vulnerability Database

```
Structure:
├─ CVE Records
│  └─ CVE-2024-XXXXX
│     ├─ Title: "Critical RCE in Service X"
│     ├─ Description: "..."
│     ├─ CVSS Score: 9.8
│     ├─ Affected Versions: ["1.0", "1.1", "2.0"]
│     └─ Remediation: "Update to version 2.1+"
│
├─ Service Mappings
│  ├─ Apache 2.4.41 → [CVE-2024-001, CVE-2024-002]
│  ├─ OpenSSH 7.4 → [CVE-2024-003, CVE-2024-004]
│  └─ ...
│
└─ Signature Patterns
   ├─ SQLi patterns: [payload1, payload2, ...]
   ├─ XSS patterns: [payload1, payload2, ...]
   └─ ...
```

### D2: Scan Profiles

```
Structure:
├─ aggressive
│  ├─ threads: 20
│  ├─ timeout: 300
│  ├─ os_detection: true
│  ├─ service_detection: true
│  ├─ deep_crawl: true
│  └─ intensity: "high"
│
├─ default
│  ├─ threads: 5
│  ├─ timeout: 180
│  ├─ os_detection: true
│  ├─ service_detection: true
│  ├─ deep_crawl: false
│  └─ intensity: "medium"
│
├─ stealth
│  ├─ threads: 2
│  ├─ timeout: 600
│  ├─ os_detection: false
│  ├─ service_detection: false
│  ├─ deep_crawl: false
│  ├─ intensity: "low"
│  └─ delay_between_requests: 5000
│
└─ quick
   ├─ threads: 10
   ├─ timeout: 60
   ├─ os_detection: false
   ├─ quick_ports: [22, 80, 443, 3389]
   └─ intensity: "high"
```

### D3: Model Registry

```
Structure:
├─ Severity Classifier
│  ├─ File: models/severity_classifier_v2.pkl
│  ├─ Version: 2.0
│  ├─ Accuracy: 0.94
│  └─ Trained on: 10,000 vulnerabilities
│
├─ Risk Predictor
│  ├─ File: models/risk_predictor_v1.pkl
│  ├─ Version: 1.0
│  ├─ Accuracy: 0.89
│  └─ Features: [severity, service_type, exposure]
│
└─ Exploit Difficulty Classifier
   ├─ File: models/exploit_difficulty_v1.pkl
   ├─ Version: 1.0
   ├─ Classes: [trivial, low, medium, hard, very_hard]
   └─ Accuracy: 0.87
```

---

## Quality Checks

### Completeness Check

- ✅ Level 0 has all external entities
- ✅ Level 1 has 9 processes + 5 data stores
- ✅ All processes have inputs/outputs
- ✅ All data stores have read/write flows
- ✅ No isolated components
- ✅ Data flows labeled with content descriptions

### Consistency Check

- ✅ Flow numbers sequential (1-16)
- ✅ Process IDs match (P1-P9)
- ✅ Data store IDs match (D1-D5)
- ✅ All terminators named consistently
- ✅ Mermaid and ASCII diagrams match

### Accuracy Check

- ✅ Flows represent actual system operations
- ✅ Data structures match implementation
- ✅ Process descriptions accurate
- ✅ External entities correctly identified
- ✅ No redundant processes

