python3 - <<'PY'
import json, os, html, urllib.parse
import platform
import subprocess
from collections import defaultdict
import shutil

# Paths
in_path = "artifacts/juice_scan_report.json"
out_dir = "artifacts"
out_path = os.path.join(out_dir, "xbow_report.html")
os.makedirs(out_dir, exist_ok=True)

# Load scan data
with open(in_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize severities
for item in data:
    item["severity"] = item.get("severity","P3").upper()
    if item["severity"] not in ["P1","P2","P3"]:
        item["severity"] = "P3"

# Severity color mapping
severity_color = {"P1":"#a00","P2":"#e67e22","P3":"#f1c40f"}

# Environment details
def safe_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return "Not available"

php_version = safe_cmd(["php","-v"]).splitlines()[0] if shutil.which("php") else "PHP not installed"
web_server = "Unknown"
os_info = f"{platform.system()} {platform.release()} ({platform.platform()})"
python_ver = platform.python_version()
env_info = f"<ul><li>OS: {os_info}</li><li>Python: {python_ver}</li><li>PHP: {php_version}</li><li>Web Server: {web_server}</li></ul>"

# Context function
def get_context(item):
    title = item.get("title","").lower()
    if "reverse php" in title:
        return "Allows remote execution of arbitrary PHP code, potentially full server compromise in a real environment."
    elif "php" in title:
        return "Unvalidated PHP input could allow attackers to execute arbitrary code, manipulate application behavior, or access sensitive data."
    else:
        return "Lab simulation; context not applicable."

# Count occurrences and files affected per bug type & severity
bug_summary = defaultdict(lambda: {"count":0, "files":set(), "severity_loop": {"P1":0,"P2":0,"P3":0}})
for item in data:
    title = item.get("title","").lower()
    if "reverse php" in title:
        bug_type = "Reverse PHP Injection"
    elif "php" in title:
        bug_type = "PHP Injection"
    else:
        bug_type = "Other"
    bug_summary[bug_type]["count"] += 1
    bug_summary[bug_type]["files"].add(item.get("file","Unknown"))
    sev = item.get("severity","P3")
    bug_summary[bug_type]["severity_loop"][sev] += 1

# Build summary table HTML
summary_html = "<h2>Vulnerability Summary</h2><table><thead><tr><th>Bug Type</th><th>Total</th><th>P1</th><th>P2</th><th>P3</th><th>Files Affected</th></tr></thead><tbody>"
for bug_type, info in bug_summary.items():
    p1 = info["severity_loop"]["P1"]
    p2 = info["severity_loop"]["P2"]
    p3 = info["severity_loop"]["P3"]
    files = ', '.join(html.escape(f) for f in info["files"])
    summary_html += f"<tr><td>{html.escape(bug_type)}</td><td>{info['count']}</td><td style='color:{severity_color['P1']}; font-weight:700'>{p1}</td><td style='color:{severity_color['P2']}; font-weight:700'>{p2}</td><td style='color:{severity_color['P3']}; font-weight:700'>{p3}</td><td>{files}</td></tr>"
summary_html += "</tbody></table>"

# Build per-file detailed HTML (collapsible)
file_vulns = defaultdict(list)
for item in data:
    file_vulns[item.get("file","Unknown")].append(item)

html_rows = []
counter = 1
for file_path, vulns in file_vulns.items():
    details_html = ""
    for it in vulns:
        title = html.escape(it.get("title",""))
        severity = it.get("severity","P3")
        severity_style = f"color:{severity_color.get(severity,'#000')}; font-weight:700;"
        line = html.escape(str(it.get("line","")))
        desc = html.escape(it.get("description",""))
        snippet = html.escape(it.get("code",""))
        recommendation = html.escape(it.get("recommendation",""))
        context = get_context(it)
        bug_type = "Other"
        vuln_html = ""
        if "reverse php" in title.lower():
            bug_type = "Reverse PHP Injection"
            vuln_html = '<span class="vuln-php reverse">Reverse PHP Injection</span>'
        elif "php" in title.lower():
            bug_type = "PHP Injection"
            vuln_html = '<span class="vuln-php">PHP Injection</span>'
        actual_result = snippet if snippet else "No code snippet available"

        details_html += f"""
        <div style="margin-bottom:10px;padding:8px;border:1px solid #ccc;border-radius:4px;">
          <strong>{title}</strong> | <span style="{severity_style}">{severity}</span> | {bug_type}<br/>
          Line: {line}<br/>
          <strong>Context:</strong> {context}<br/>
          <strong>Environment:</strong> {env_info}<br/>
          <strong>Actual Result:</strong> <pre>{actual_result}</pre>
          <strong>Description:</strong> <pre>{desc}</pre>
          Recommendation: {recommendation}<br/>
          {vuln_html}<br/>
          <a href="mailto:?subject={urllib.parse.quote(title)}">Report bug</a>
        </div>
        """

    html_rows.append(f"""
    <tr>
      <td>{counter}</td>
      <td colspan="11">
        <details class="vuln-details">
          <summary style="font-weight:bold;">File: {html.escape(file_path)} ({len(vulns)} vulnerabilities)</summary>
          {details_html}
        </details>
      </td>
    </tr>
    """)
    counter += 1

# Header with expand/collapse all buttons
header = f"""<!doctype html>
<html><head><meta charset="utf-8"/><title>X-Bow style scan results</title>
<style>
 body{{font-family:Arial,sans-serif;background:#f3f6fb;color:#222;padding:20px;}}
 table{{width:100%;border-collapse:collapse;margin-bottom:20px;}}
 th,td{{padding:8px;border-bottom:1px solid #eee;vertical-align:top;}}
 th{{background:#fafafa;}}
 .vuln-php{{color:#900;font-weight:700;margin-left:8px;}}
 .reverse{{text-decoration:underline;}}
 pre{{margin:0;font-family:monospace;font-size:12px;white-space:pre-wrap;background:#f8f8f8;border-radius:4px;padding:6px;}}
 details{{margin-bottom:10px;}}
 summary{{cursor:pointer;}}
 .btn{{padding:6px 12px;margin:4px;cursor:pointer;background:#3498db;color:#fff;border:none;border-radius:4px;}}
</style>
<script>
function expandAll(){{document.querySelectorAll('details.vuln-details').forEach(d=>d.open=true);}}
function collapseAll(){{document.querySelectorAll('details.vuln-details').forEach(d=>d.open=false);}}
</script>
</head><body>
<h1>X-Bow style scan results</h1>
<div>
<button class="btn" onclick="expandAll()">Expand All</button>
<button class="btn" onclick="collapseAll()">Collapse All</button>
</div>
<h2>Environment Summary</h2>{env_info}
{summary_html}
<table><thead><tr><th>#</th><th colspan="11">File / Vulnerabilities</th></tr></thead><tbody>"""

footer = "</tbody></table></body></html>"

with open(out_path, "w", encoding="utf-8") as f:
    f.write(header)
    f.write("\n".join(html_rows))
    f.write(footer)

print("[*] Generated full X-Bow report with Expand/Collapse All and severity loop at:", out_path)
PY
