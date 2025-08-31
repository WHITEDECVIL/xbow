import json

simulated_findings = [
  {
    "title": "Simulated Reverse PHP Injection",
    "severity": "P1",
    "file": "artifacts/reverse_php_injection_placeholder.php",
    "line": 1,
    "description": "This is a simulated Reverse PHP Injection payload for lab purposes.",
    "code": "<?php echo 'Simulated Reverse PHP Injection'; ?>",
    "recommendation": "Review code handling user input; this is a lab simulation."
  },
  {
    "title": "Simulated PHP Injection",
    "severity": "P2",
    "file": "artifacts/php_injection_placeholder.php",
    "line": 1,
    "description": "This is a simulated PHP Injection payload for lab purposes.",
    "code": "<?php echo 'Simulated PHP Injection'; ?>",
    "recommendation": "Validate and sanitize all user input; this is a lab simulation."
  }
]

# You can now pass `simulated_findings` to your report generator function
# For example:
generate_xbow_report(simulated_findings)

