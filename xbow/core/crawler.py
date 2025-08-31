import requests
from bs4 import BeautifulSoup

def run(url):
    findings = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        for link in links:
            findings.append({
                "type": "Link",
                "param": "-",
                "severity": "Info",
                "vrt": "Information Disclosure",
                "details": link
            })
    except Exception as e:
        findings.append({
            "type": "Error",
            "param": "-",
            "severity": "Info",
            "vrt": "N/A",
            "details": str(e)
        })
    return findings

