import os

def normalize_finding(f):
    """Ensure every finding is a dict with safe defaults."""
    if isinstance(f, str):
        return {
            "type": "Info",
            "param": "-",
            "severity": "Info",
            "vrt": "N/A",
            "details": f
        }
    return f

def save_markdown(url, results, outdir):
    lines = [f"# XBOW Report for {url}\n"]

    for section, findings in results.items():
        lines.append(f"## {section.capitalize()} Findings")
        for f in findings:
            f = normalize_finding(f)   # 🔑 FIX
            lines.append(
                f"- **Type:** {f.get('type','Unknown')}, "
                f"**Param:** {f.get('param','-')}, "
                f"**Severity:** {f.get('severity','-')}, "
                f"**VRT:** {f.get('vrt','-')}, "
                f"**Details:** {f.get('details','')}"
            )
        lines.append("")

    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(
        outdir, url.replace("https://","").replace("http://","").replace("/","_") + ".md"
    )
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"[+] Markdown report saved: {path}")


def save_html(url, results, outdir):
    html = [f"<html><head><title>XBOW Report for {url}</title></head><body>"]
    html.append(f"<h1>XBOW Report for {url}</h1>")

    for section, findings in results.items():
        html.append(f"<h2>{section.capitalize()} Findings</h2><ul>")
        for f in findings:
            f = normalize_finding(f)   # 🔑 FIX
            html.append(
                f"<li><b>Type:</b> {f.get('type','Unknown')} | "
                f"<b>Param:</b> {f.get('param','-')} | "
                f"<b>Severity:</b> {f.get('severity','-')} | "
                f"<b>VRT:</b> {f.get('vrt','-')} | "
                f"<b>Details:</b> {f.get('details','')}</li>"
            )
        html.append("</ul>")

    html.append("</body></html>")

    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(
        outdir, url.replace("https://","").replace("http://","").replace("/","_") + ".html"
    )
    with open(path, "w") as f:
        f.write("\n".join(html))
    print(f"[+] HTML report saved: {path}")

