"""
Report Generation Module - HTML and PDF Reports
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from jinja2 import Template

from src.utils.logger import logger, color_logger


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>XBOW Penetration Test Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 40px; }
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 { color: #2c3e50; font-size: 32px; }
        .header p { color: #7f8c8d; margin-top: 10px; }
        .summary {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-box {
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            color: white;
        }
        .summary-box.critical { background-color: #e74c3c; }
        .summary-box.high { background-color: #e67e22; }
        .summary-box.medium { background-color: #f39c12; }
        .summary-box.low { background-color: #27ae60; }
        .summary-box h3 { font-size: 24px; margin-bottom: 5px; }
        .summary-box p { font-size: 12px; }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .vulnerability {
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #ecf0f1;
            border-radius: 3px;
        }
        .vulnerability.high { border-left-color: #e67e22; }
        .vulnerability.medium { border-left-color: #f39c12; }
        .vulnerability.low { border-left-color: #27ae60; }
        .vulnerability h4 { margin-bottom: 10px; color: #2c3e50; }
        .vulnerability-details {
            font-size: 13px;
            color: #555;
        }
        .vulnerability-details p { margin: 5px 0; }
        .severity-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }
        .severity-badge.critical { background-color: #e74c3c; }
        .severity-badge.high { background-color: #e67e22; }
        .severity-badge.medium { background-color: #f39c12; }
        .severity-badge.low { background-color: #27ae60; }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #bdc3c7;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        table th, table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #bdc3c7;
        }
        table th { background-color: #ecf0f1; font-weight: bold; }
        .remediation {
            background-color: #d5f4e6;
            padding: 10px;
            border-radius: 3px;
            margin-top: 10px;
            border-left: 3px solid #27ae60;
        }
        .page-break { page-break-after: always; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Penetration Test Report</h1>
            <p>XBOW - Professional Security Assessment</p>
            <p>Generated: {{ timestamp }}</p>
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            <p><strong>Target:</strong> {{ target }}</p>
            <p><strong>Scan Type:</strong> {{ scan_type }}</p>
            <p><strong>Overall Risk Level:</strong> <span class="severity-badge {{ risk_level }}">{{ risk_level }}</span></p>
            <p><strong>Total Vulnerabilities Found:</strong> {{ total_vulnerabilities }}</p>
        </div>

        <div class="summary">
            <div class="summary-box critical">
                <h3>{{ critical_count }}</h3>
                <p>Critical</p>
            </div>
            <div class="summary-box high">
                <h3>{{ high_count }}</h3>
                <p>High</p>
            </div>
            <div class="summary-box medium">
                <h3>{{ medium_count }}</h3>
                <p>Medium</p>
            </div>
            <div class="summary-box low">
                <h3>{{ low_count }}</h3>
                <p>Low</p>
            </div>
        </div>

        {% if vulnerabilities %}
        <div class="section">
            <h2>Findings</h2>
            {% for vuln in vulnerabilities %}
            <div class="vulnerability {{ vuln.severity|lower }}">
                <h4>
                    <span class="severity-badge {{ vuln.severity|lower }}">{{ vuln.severity }}</span>
                    {{ vuln.name }}
                </h4>
                <div class="vulnerability-details">
                    {% if vuln.url %}
                    <p><strong>URL:</strong> {{ vuln.url }}</p>
                    {% endif %}
                    {% if vuln.description %}
                    <p><strong>Description:</strong> {{ vuln.description }}</p>
                    {% endif %}
                    {% if vuln.cwe %}
                    <p><strong>CWE:</strong> {{ vuln.cwe }}</p>
                    {% endif %}
                    {% if vuln.owasp %}
                    <p><strong>OWASP:</strong> {{ vuln.owasp }}</p>
                    {% endif %}
                    {% if vuln.detection_method %}
                    <p><strong>Detection:</strong> {{ vuln.detection_method }} (confidence: {{ '%.2f' % vuln.confidence }})</p>
                    {% endif %}
                    {% if vuln.poc %}
                    <p><strong>PoC Payload:</strong> <code>{{ vuln.poc }}</code></p>
                    {% endif %}
                    {% if vuln.payload_type %}
                    <p><strong>Payload Type:</strong> {{ vuln.payload_type }}</p>
                    {% endif %}
                    {% if vuln.exploitation_method %}
                    <p><strong>Exploitation Method:</strong> {{ vuln.exploitation_method }}</p>
                    {% endif %}
                    {% if vuln.how_exploit_works %}
                    <p><strong>How Exploit Works:</strong> {{ vuln.how_exploit_works }}</p>
                    {% endif %}
                    {% if vuln.poc_response_status or vuln.poc_response %}
                    <p><strong>PoC Response:</strong> Status {{ vuln.poc_response_status }}<br>
                    <pre style="white-space:pre-wrap; max-height:200px; overflow:auto; background:#fff; padding:8px; border:1px solid #ddd;">{{ vuln.poc_response }}</pre></p>
                    {% endif %}
                    {% if vuln.remediation %}
                    <div class="remediation">
                        <strong>Remediation:</strong> {{ vuln.remediation }}
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if recommendations %}
        <div class="section">
            <h2>Recommendations</h2>
            <ul>
            {% for rec in recommendations %}
                <li>{{ rec }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endif %}

        <div class="footer">
            <p>This report is confidential and intended for authorized personnel only.</p>
            <p>XBOW Penetration Testing Framework &copy; 2024</p>
        </div>
    </div>
</body>
</html>
"""


class ReportGenerator:
    """Generates HTML and JSON reports"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, findings: Dict, filename: str = None) -> str:
        """Generate HTML report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pentest_report_{timestamp}.html"
        
        report_path = self.output_dir / filename
        
        # Count vulnerabilities by severity
        vulnerabilities = findings.get('vulnerabilities', [])
        severity_counts = {
            'critical': len([v for v in vulnerabilities if v.get('severity') == 'CRITICAL']),
            'high': len([v for v in vulnerabilities if v.get('severity') == 'HIGH']),
            'medium': len([v for v in vulnerabilities if v.get('severity') == 'MEDIUM']),
            'low': len([v for v in vulnerabilities if v.get('severity') == 'LOW']),
        }
        
        # Prepare data for template
        data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'target': findings.get('target', 'Unknown'),
            'scan_type': findings.get('scan_type', 'Full Pentest'),
            'risk_level': findings.get('risk_level', 'MEDIUM'),
            'total_vulnerabilities': len(vulnerabilities),
            'critical_count': severity_counts['critical'],
            'high_count': severity_counts['high'],
            'medium_count': severity_counts['medium'],
            'low_count': severity_counts['low'],
            'vulnerabilities': vulnerabilities,
            'recommendations': self._generate_recommendations(vulnerabilities),
        }
        
        # Render template
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**data)
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        color_logger.success(f"HTML report generated: {report_path}", "REPORT")
        return str(report_path)
    
    def generate_json_report(self, findings: Dict, filename: str = None) -> str:
        """Generate JSON report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pentest_report_{timestamp}.json"
        
        report_path = self.output_dir / filename
        
        report_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'tool': 'XBOW',
                'version': '1.0.0',
            },
            **findings
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        color_logger.success(f"JSON report generated: {report_path}", "REPORT")
        return str(report_path)
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []
        
        if not vulnerabilities:
            recommendations.append("No vulnerabilities found. System appears secure.")
            return recommendations
        
        severity_map = {
            'CRITICAL': 5,
            'HIGH': 4,
            'MEDIUM': 3,
            'LOW': 2,
            'INFO': 1,
        }
        
        critical_vulns = [v for v in vulnerabilities 
                         if severity_map.get(v.get('severity'), 0) >= 4]
        
        if critical_vulns:
            recommendations.append("Address CRITICAL and HIGH severity vulnerabilities immediately")
        
        # Check for injection vulnerabilities
        if any('injection' in v.get('name', '').lower() for v in vulnerabilities):
            recommendations.append("Implement input validation and parameterized queries to prevent injection attacks")
        
        # Check for authentication issues
        if any('auth' in v.get('name', '').lower() for v in vulnerabilities):
            recommendations.append("Review and strengthen authentication mechanisms")
        
        # Check for configuration issues
        if any('misconfiguration' in v.get('name', '').lower() or 
               'missing' in v.get('name', '').lower() for v in vulnerabilities):
            recommendations.append("Review security configuration and apply security hardening guidelines")
        
        # Check for SSL/TLS issues
        if any('ssl' in v.get('name', '').lower() or 'tls' in v.get('name', '').lower() 
               for v in vulnerabilities):
            recommendations.append("Upgrade to modern TLS versions and disable legacy protocols")
        
        recommendations.append("Implement a Web Application Firewall (WAF)")
        recommendations.append("Perform regular security assessments and penetration tests")
        recommendations.append("Implement security monitoring and incident response procedures")
        
        return recommendations
