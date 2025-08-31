import requests

def run(url):
    findings = []
    wordlist = ["admin", "login", "robots.txt", "sitemap.xml"]
    for w in wordlist:
        test_url = url.rstrip("/") + "/" + w
        try:
            r = requests.get(test_url, timeout=5)
            if r.status_code in [200, 301, 302, 403]:
                findings.append({
                    "type": "Dir/File",
                    "param": w,
                    "severity": "Info",
                    "vrt": "Directory Enumeration",
                    "details": f"{test_url} (status={r.status_code})"
                })
        except Exception as e:
            findings.append({
                "type": "Error",
                "param": w,
                "severity": "Info",
                "vrt": "N/A",
                "details": str(e)
            })
    return findings

