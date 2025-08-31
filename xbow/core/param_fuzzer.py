import requests

def run(url):
    findings = []
    params = ["id", "q", "search", "file", "redirect"]
    for p in params:
        test_url = f"{url}?{p}=test"
        try:
            r = requests.get(test_url, timeout=5)
            if "test" in r.text:
                findings.append({
                    "type": "Reflected Param",
                    "param": p,
                    "severity": "Medium",
                    "vrt": "Reflected XSS",
                    "details": f"Parameter {p} reflected at {test_url}"
                })
        except Exception as e:
            findings.append({
                "type": "Error",
                "param": p,
                "severity": "Info",
                "vrt": "N/A",
                "details": str(e)
            })
    return findings

