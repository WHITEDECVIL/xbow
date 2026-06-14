<div align="center">

<!-- Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=venom&color=0:0d1117,50:003300,100:00ff41&height=200&section=header&text=XBOW&fontSize=90&fontColor=00ff41&fontAlignY=55&desc=AI-Powered%20Penetration%20Testing%20Framework&descSize=18&descAlignY=75&descColor=ffffff&animation=twinkling" />

<!-- Badges Row 1 -->
<br/>

![Python](https://img.shields.io/badge/Python-3.9+-00ff41?style=for-the-badge&logo=python&logoColor=00ff41&labelColor=0d1117)
![AI Powered](https://img.shields.io/badge/AI-Powered-00ff41?style=for-the-badge&logo=openai&logoColor=00ff41&labelColor=0d1117)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge&labelColor=0d1117)
![Platform](https://img.shields.io/badge/Platform-Linux%20|%20Kali-00ff41?style=for-the-badge&logo=linux&logoColor=00ff41&labelColor=0d1117)

<!-- Badges Row 2 -->

![Stars](https://img.shields.io/github/stars/WHITEDECVIL/XBOW?style=for-the-badge&logo=github&color=00ff41&labelColor=0d1117)
![Issues](https://img.shields.io/github/issues/WHITEDECVIL/XBOW?style=for-the-badge&color=ff4444&labelColor=0d1117)
![Last Commit](https://img.shields.io/github/last-commit/WHITEDECVIL/XBOW?style=for-the-badge&color=00ff41&labelColor=0d1117)
![Repo Size](https://img.shields.io/github/repo-size/WHITEDECVIL/XBOW?style=for-the-badge&color=00ff41&labelColor=0d1117)

<br/>

```
██╗  ██╗██████╗  ██████╗ ██╗    ██╗
╚██╗██╔╝██╔══██╗██╔═══██╗██║    ██║
 ╚███╔╝ ██████╔╝██║   ██║██║ █╗ ██║
 ██╔██╗ ██╔══██╗██║   ██║██║███╗██║
██╔╝ ██╗██████╔╝╚██████╔╝╚███╔███╔╝
╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝
   [ AI-Powered Penetration Testing ]
```

*"The quieter you become, the more vulnerabilities you hear."*

</div>

---

<div align="center">

## ⚡ What is XBOW?

</div>

**XBOW** is a professional-grade, AI-driven penetration testing framework built for **security researchers, red teamers, and bug bounty hunters**. It automates reconnaissance, vulnerability scanning, and exploitation workflows — with an intelligent ML layer that classifies and prioritizes threats in real time.

> ⚠️ **Legal Notice:** This tool is strictly for **authorized security testing only**. Unauthorized use against systems you do not own or have explicit written permission to test is **illegal**. The author holds no responsibility for misuse.

---

## 🗂️ Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Scan Modes](#-scan-modes)
- [Live Interactive Shell](#-live-interactive-shell)
- [AI Automated Mode](#-ai-automated-mode)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Dependencies](#-dependencies)

---

## 🔥 Features

<table>
<tr>
<td width="50%">

**🌐 Scanning & Recon**
- Advanced host discovery & port scanning
- Web application vulnerability scanning
- DNS enumeration & subdomain discovery
- Multi-protocol: TCP, UDP, HTTP/HTTPS, DNS

</td>
<td width="50%">

**🤖 AI & Intelligence**
- ML-based vulnerability classification
- Severity prediction & risk scoring
- Adaptive scanning based on findings
- External AI agent plugin support

</td>
</tr>
<tr>
<td width="50%">

**💥 Exploitation**
- Interactive real-time exploit shell
- Safe-mode exploitation framework
- nmap, sqlmap, nikto, dirb, metasploit integration
- Session persistence with vuln ID tracking

</td>
<td width="50%">

**📊 Reporting**
- Professional HTML & PDF report generation
- Integrated CVE & vulnerability database
- Real-time logging & audit trails
- Predefined & custom scan profiles

</td>
</tr>
</table>

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/WHITEDECVIL/XBOW.git
cd XBOW

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -m xbow --help
```

---

## ⚡ Quick Start

```bash
# 🔍 Network scan
xbow scan --target 192.168.1.0/24 --scan-type network

# 🌐 Web vulnerability scan
xbow scan --target https://example.com --scan-type web

# 💣 Full penetration test with report
xbow pentest --target example.com --profile aggressive --generate-report

# 🔎 DNS enumeration
xbow enumerate --target example.com

# 🤖 AI automated pentesting
xbow live --target https://example.com --mode auto --duration 300

# 🧠 AI agent-assisted pentesting
xbow live --target https://example.com --mode auto --enable-ai-agent --duration 300
```

---

## 🖥️ Scan Modes

| Mode | Command | Description |
|------|---------|-------------|
| 🔍 **Network** | `--scan-type network` | Host discovery, port scanning |
| 🌐 **Web** | `--scan-type web` | Web app vulnerability testing |
| 🔎 **DNS** | `enumerate` | Subdomain & DNS reconnaissance |
| 💬 **Interactive** | `--mode interactive` | Live shell with real-time results |
| 👁️ **Monitor** | `--mode monitor` | Passive real-time monitoring |
| 🤖 **Auto** | `--mode auto` | Full AI-driven automation |

---

## 🖥️ Live Interactive Shell

Start a real-time hacking session with full shell access:

```bash
xbow live --target https://example.com --mode interactive
```

### Available Shell Commands

```
┌─[XBOW]─[interactive]─[target: example.com]
│
├── scan web          →  Scan for web vulnerabilities
├── list              →  List found vulns with IDs
├── exploit <id>      →  Attempt exploitation of vuln by ID
├── nmap -p 80,443    →  Run nmap scan inline
├── sqlmap -u <URL>   →  Run SQLMap injection test
├── info              →  Show target information
├── help              →  Show all available commands
└── quit              →  Exit session
```

**Shell Features:**
- 🔒 **Safe Exploitation** — all exploits run in safe mode, no actual damage
- 🧩 **Session Persistence** — vulnerabilities tracked with unique IDs across the session
- 🔧 **Multi-Tool Integration** — nmap, sqlmap, nikto, dirb, metasploit built-in
- ⚡ **Real-time Feedback** — immediate results on every scan and exploit attempt

---

## 🤖 AI Automated Mode

Let XBOW's intelligence layer drive the entire pentest:

```bash
xbow live --target https://example.com --mode auto --enable-ai-agent --duration 300
```

**How the AI decides:**

```
Target Discovered
      │
      ▼
┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Port Scan  │────▶│  AI Classification│────▶│  Adaptive Scanning │
└─────────────┘     └──────────────────┘     └────────────────────┘
                                                        │
                              ┌─────────────────────────┘
                              ▼
                   ┌─────────────────────┐     ┌──────────────────┐
                   │ Vulnerability Found  │────▶│ Exploit Decision  │
                   └─────────────────────┘     └──────────────────┘
                                                        │
                              ┌─────────────────────────┘
                              ▼
                   ┌─────────────────────┐
                   │  Report Generation   │
                   └─────────────────────┘
```

**AI Capabilities:**
- 🧠 Intelligent scan-type selection based on live findings
- 🎯 Prioritizes high-severity vulnerabilities for exploitation
- 🔄 Iterative — re-scans based on what it discovers
- 📋 Generates detailed automated action summary report

---

## 📁 Project Structure

```
XBOW/
├── 📂 src/
│   ├── 📄 __init__.py
│   ├── 📄 cli.py                    # Command-line interface
│   ├── 📂 scanner/                  # Core scanning engines
│   │   ├── network.py               # Host & port discovery
│   │   ├── web.py                   # Web vuln scanner
│   │   ├── dns.py                   # DNS enumeration
│   │   └── vulnerability.py         # CVE matching
│   ├── 📂 ai_engine/                # ML/AI analysis layer
│   │   ├── classifier.py            # Vulnerability classification
│   │   ├── predictor.py             # Severity prediction
│   │   └── models/                  # Trained ML models
│   ├── 📂 exploits/                 # Exploitation framework
│   │   ├── base.py
│   │   └── payloads/
│   ├── 📂 reporting/                # Report generation
│   │   ├── html_report.py
│   │   ├── pdf_report.py
│   │   └── templates/
│   ├── 📂 utils/                    # Helpers & config
│   │   ├── logger.py
│   │   ├── config.py
│   │   └── helpers.py
│   └── 📂 database/                 # Vulnerability DB
├── 📂 config/
│   ├── xbow.cfg
│   ├── profiles.json
│   └── cve_database.json
├── 📂 tests/
├── 📂 docs/
├── 📄 requirements.txt
├── 📄 setup.py
└── 📄 LICENSE
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                      CLI Layer                       │
│           User Interface & Command Handling          │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Scanning │  │  AI / ML │  │ Exploits │
   │  Layer   │  │  Layer   │  │  Layer   │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              ┌─────────────────┐
              │  Reporting Layer │
              │  HTML / PDF      │
              └─────────────────┘
```

---

## 📚 Dependencies

```bash
# Core
Python 3.9+

# Network Tools (system)
nmap
masscan

# Python Packages
scikit-learn        # ML classification
tensorflow          # Deep learning models
selenium            # Web automation
requests            # HTTP client
jinja2              # Report templating
weasyprint          # PDF generation
```

---

## 📊 Language Breakdown

<div align="center">

![Python](https://img.shields.io/badge/Python-50.7%25-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117)
![TeX](https://img.shields.io/badge/TeX-47.8%25-008080?style=for-the-badge&logo=latex&logoColor=white&labelColor=0d1117)
![Shell](https://img.shields.io/badge/Shell-1.1%25-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white&labelColor=0d1117)
![Makefile](https://img.shields.io/badge/Makefile-0.4%25-6D8086?style=for-the-badge&logo=cmake&logoColor=white&labelColor=0d1117)

</div>

---

## 👤 Author

<div align="center">

**Sanjay S** — *Cybersecurity Researcher & Red Teamer*

[![GitHub](https://img.shields.io/badge/GitHub-WHITEDECVIL-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117)](https://github.com/WHITEDECVIL)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sanjay_S-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0d1117)](https://linkedin.com/in/sanjay-s)
[![HackerOne](https://img.shields.io/badge/HackerOne-Profile-494649?style=for-the-badge&logo=hackerone&logoColor=white&labelColor=0d1117)](https://hackerone.com)
[![Email](https://img.shields.io/badge/Email-sankicju@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0d1117)](mailto:sankicju@gmail.com)

</div>

---

<div align="center">

> **⚠️ Disclaimer:** XBOW is developed for **ethical and legal security research only**.
> Always obtain **written authorization** before testing any system.
> Misuse of this tool is a criminal offense.

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:00ff41,100:003300&height=100&section=footer" />

</div>
