import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.scanner.web import WebScanner, Vulnerability


class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        test_val = qs.get('test', [''])[0]
        body = f"echo:{test_val}"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))


def run_server(server):
    try:
        server.serve_forever()
    except Exception:
        pass


def test_execute_poc_reflection():
    # start local server on an ephemeral port
    server = HTTPServer(('127.0.0.1', 0), EchoHandler)
    port = server.server_address[1]
    t = threading.Thread(target=run_server, args=(server,), daemon=True)
    t.start()

    try:
        payload = "<script>alert('XSS')</script>"
        encoded_payload = urllib.parse.quote(payload, safe='')
        url = f"http://127.0.0.1:{port}/?id=1&test={encoded_payload}"

        scanner = WebScanner()

        vuln = Vulnerability(
            name="Test PoC",
            type="XSS",
            url=url,
            poc=payload,
            severity='HIGH',
        )

        # execute PoC
        scanner._execute_poc(vuln)

        assert vuln.poc_response_status == 200
        assert vuln.poc_response is not None
        assert payload in vuln.poc_response or payload in urllib.parse.unquote(vuln.poc_response)
        assert getattr(vuln, 'poc_confirmed', False) is True

    finally:
        server.shutdown()
        server.server_close()
