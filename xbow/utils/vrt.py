VRT_MAP = {
    "reflected_xss": {"category": "Server-Side Injection > Reflected Cross-Site Scripting (XSS)", "severity": "P3"},
    "stored_xss": {"category": "Server-Side Injection > Stored Cross-Site Scripting (XSS)", "severity": "P2"},
    "open_redirect": {"category": "Server-Side Injection > Open Redirect", "severity": "P4"},
    "sql_injection": {"category": "Server-Side Injection > SQL Injection", "severity": "P1"},
    "ssrf": {"category": "Server-Side Injection > Server-Side Request Forgery (SSRF)", "severity": "P1"},
    "dir_listing": {"category": "Sensitive Data Exposure > Directory Listing", "severity": "P4"},
    "exposed_file": {"category": "Sensitive Data Exposure > Exposed File (.git, .env, backup)", "severity": "P3"},
    "sensitive_info": {"category": "Sensitive Data Exposure > Information Disclosure", "severity": "P3"},
    "misconfig": {"category": "Security Misconfiguration", "severity": "P4"},
    "headers_injection": {"category": "Security Misconfiguration > Host Header Injection", "severity": "P3"},
    "idor": {"category": "Broken Access Control > Insecure Direct Object Reference (IDOR)", "severity": "P2"},
}

