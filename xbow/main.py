import argparse
import urllib3  # Suppress SSL warnings globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from core import crawler, dirbuster, param_fuzzer, reporter
from core import header_injector, vuln_scanner, pretty_reporter, collaborator
# Removed duplicate import of pretty_reporter
# Removed direct import of save_html to avoid confusion

def main():
    parser = argparse.ArgumentParser(description="XBOW - Automated Web Pentesting Framework")
    parser.add_argument("url", help="Target URL (e.g. https://example.com)")
    parser.add_argument("--out", default="scans", help="Output directory for reports")
    parser.add_argument(
        "--modules",
        nargs="+",
        default=["crawl", "dir", "fuzz"],
        choices=["crawl", "dir", "fuzz", "headers", "scan", "report"],
        help="Modules to run: crawl, dir, fuzz, headers, scan, report"
    )
    args = parser.parse_args()

    results = {}

    if "crawl" in args.modules:
        results["crawl"] = crawler.run(args.url)

    if "dir" in args.modules:
        results["dirs"] = dirbuster.run(args.url)

    if "fuzz" in args.modules:
        results["fuzz"] = param_fuzzer.run(args.url)

    if "headers" in args.modules:
        collab_url = collaborator.generate()
        results["headers"] = header_injector.run(args.url, payload=f"http://{collab_url}")

    if "scan" in args.modules:
        results["scans"] = vuln_scanner.run(args.url)

    if "report" in args.modules or args.out:
        reporter.save(args.url, results, args.out)                         # JSON
        pretty_reporter.save_markdown(args.url, results, args.out)        # Markdown
        pretty_reporter.save_html(args.url, results, args.out)            # HTML

if __name__ == "__main__":
    main()
