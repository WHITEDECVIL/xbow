import os, json
from utils.vrt import VRT_MAP

def normalize_severity(sev):
    """Convert various severity labels to P1, P2, P3"""
    sev = str(sev).lower()
    if sev in ("critical", "high", "p1"): return "P1"
    if sev in ("medium", "med", "p2"): return "P2"
    if sev in ("low", "info", "p3"): return "P3"
    return "P3"

def classify_finding(finding_type):
    """Map a finding to VRT category & normalized severity"""
    base = VRT_MAP.get(finding_type, {"category": "Uncategorized", "severity": "P5"})
    base["severity"] = normalize_severity(base.get("severity", "P5"))

    # Optional manual overrides for specific types
    if finding_type == "Header Injection":
        base["severity"] = "P2"
    elif finding_type == "Reverse Shell":
        base["severity"] = "P1"
    elif finding_type == "Reflected Parameter":
        base["severity"] = "P3"

    return base

def save(url, results, outdir):
    os.makedirs(outdir, exist_ok=True)
    classified = {}

    for module, findings in results.items():
        classified[module] = []
        for f in findings if isinstance(findings, list) else [findings]:
            if isinstance(f, dict) and "type" in f:
                f.update(classify_finding(f["type"]))
            classified[module].append(f)

    filename = os.path.join(outdir, url.replace("https://", "").replace("http://", "").replace("/", "_") + ".json")
    with open(filename, "w") as f:
        json.dump(classified, f, indent=2)

    print(f"[+] VRT-mapped report saved: {filename}")

