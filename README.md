# X-Bow — Automated Web Recon & Reporting

Small wrapper that orchestrates crawling, fuzzing, header injection checks, static scanning, and generates an X‑Bow style HTML/Markdown report. Includes safe simulated payload artifacts for demonstration and triage workflows.

## Features
- Crawl targets and collect pages/resources
- Fuzz common parameters for reflection/XSS
- Test header injection vectors (SSRF / header manipulation)
- Run static scanner and merge safe simulated findings
- Generate:
  - JSON scanner output: `juice_scan_report.json`
  - Artifacts and payload placeholders: `artifacts/`
  - X‑Bow HTML report: `artifacts/xbow_report.html`
  - Per-scan markdown under `scans/<target>/` (example: `scans/nasa/www.nasa.gov.md`)

## Requirements
- Linux (tested on Kali/Ubuntu)
- Python 3 (stdlib modules used: json, html, urllib, platform, subprocess, collections, shutil)
- Optional: Docker + docker-compose or Docker Compose plugin (only if you want to start lab containers)

## Quick start
1. Make scripts executable:
```bash
chmod +x run.sh
```

2. Run (skip container startup if docker/compose not installed):
```bash
# Start containers if available
./run.sh https://example.com --modules crawl fuzz headers scan report --out scans/example

# Skip starting containers (no docker required)
SKIP_CONTAINERS=1 ./run.sh https://example.com --modules crawl fuzz headers scan report --out scans/example

# Or invoke with bash
SKIP_CONTAINERS=1 bash run.sh https://example.com --modules crawl fuzz headers scan report --out scans/example
```

3. Open generated report:
```bash
xdg-open artifacts/xbow_report.html
```

## Project layout
- run.sh — main orchestration script (crawl → scan → inject simulated findings → HTML report)
- crawler.py — crawler (called by run.sh)
- static_scanner.py — static scanning wrapper (called by run.sh)
- artifacts/ — downloaded pages, simulated payloads, xbow_report.html
- juice_scan_report.json — scanner output + injected simulated findings
- scans/ — per-target markdown reports (example provided for NASA)

## Notes & caveats
- Simulated payloads are clearly labeled and safe for lab/demo only (e.g. `artifacts/php_injection_placeholder.php`).
- Ensure you have permission to test any external target. Use only against authorized systems.
- If you see zsh paste issues when editing scripts (history expansion with `!`), disable bang-history: `setopt NO_BANG_HIST` or write files using a quoted heredoc.

## Troubleshooting
- run.sh: command not found — run with `./run.sh` or `bash run.sh` or add current dir to PATH.
- Docker missing — install Docker + docker-compose-plugin, or run with `SKIP_CONTAINERS=1`.
- Python errors — verify Python 3 is installed and available as `python3`.

## Contributing
- Fixes and improvements welcome. Keep simulated payloads clearly marked safe.
- Follow responsible disclosure and do not add real exploit payloads.

## License & Disclaimer
- Use at your own risk. This tool includes safe simulated findings only.
- Do not scan systems
