import requests

HEADERS_TO_TEST = [
    ("Referer", "P3"),           # Often used for tracking; low risk
    ("X-Forwarded-For", "P2"),   # Can spoof IP; medium risk
    ("X-Host", "P2"),            # May affect routing; medium risk
    ("X-Original-URL", "P1"),    # Can influence backend logic; high risk
    ("X-Client-IP", "P1")        # Can spoof client identity; high risk
]

def run(url, payload="http://collab.example.com"):
    findings = []
    for header, severity in HEADERS_TO_TEST:
        try:
            r = requests.get(url, headers={header: payload}, timeout=5)
            findings.append({
                "type": "Header Injection",
                "param": header,
                "severity": severity,
                "vrt": "Potential SSRF / Header Manipulation",
                "details": f"Injected {header} with payload {payload}, status={r.status_code}"
            })
        except Exception as e:
            findings.append({
                "type": "Error",
                "param": header,
                "severity": "P3",
                "vrt": "N/A",
                "details": str(e)
            })
    return findings

