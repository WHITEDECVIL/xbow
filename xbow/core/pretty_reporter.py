import os
from datetime import datetime

def save_markdown(url, results, outdir):
    os.makedirs(outdir, exist_ok=True)
    filename = os.path.join(outdir, url.replace("https://", "").replace("http://", "").replace("/", "_") + ".md")

    lines = []
    lines.append(f"# XBOW Report for {url}")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

    severity_emojis = {
        "P1": "🟥 Critical",
        "P2": "🟧 Medium",
        "P3": "🟩 Low"
    }

    for module, findings in results.items():
        if not findings:
            continue
        lines.append(f"## {module.upper()}")
        for f in findings:
            sev = f.get("severity", "P5")
            badge = severity_emojis.get(sev, sev)
            lines.append(f"- **Type:** {f.get('type','Unknown')}")
            lines.append(f"  - **Category (VRT):** {f.get('category','Uncategorized')}")
            lines.append(f"  - **Severity:** {badge}")
            for k, v in f.items():
                if k not in ["type", "category", "severity"]:
                    lines.append(f"  - **{k}:** {v}")
            lines.append("")

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    print(f"[+] Markdown report saved: {filename}")

def save_html(url, results, out_dir):
    import os
    from datetime import datetime

    domain = url.replace("https://", "").replace("http://", "").strip("/")
    filename = os.path.join(out_dir, f"{domain}.html")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>XBOW Report - {domain}</title>
    <style>
        body {{ font-family: sans-serif; padding: 20px; }}
        h2 {{ color: #2c3e50; }}
        .section {{ margin-bottom: 30px; }}
        .severity-high {{ color: red; }}
        .severity-medium {{ color: orange; }}
        .severity-low {{ color: green; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Scan Report for {domain}</h1>
    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

    for key, value in results.items():
        html += f"<div class='section'><h2>{key.title()}</h2><pre>{str(value)}</pre></div>\n"

    html += "</body></html>"

    os.makedirs(out_dir, exist_ok=True)
    with open(filename, "w") as f:
        f.write(html)
    print(f"[+] HTML report saved: {filename}")
