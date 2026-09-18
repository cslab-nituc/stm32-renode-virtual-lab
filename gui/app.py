"""Local, single-user Virtual Lab HTTP server. Python 3.10+; stdlib only."""
import json
import os
from pathlib import Path
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'bridge'))
from protocol import validate_input


class BridgeClient:
    def __init__(self, port=4567):
        self.port = port
        self.lock = threading.Lock()
        self.sock = None
        self.reader = None

    def close(self):
        if self.reader:
            self.reader.close()
        if self.sock:
            self.sock.close()
        self.reader = self.sock = None

    def request(self, message):
        with self.lock:
            try:
                if self.sock is None:
                    self.sock = socket.create_connection(('127.0.0.1', self.port), timeout=1)
                    self.reader = self.sock.makefile('rb')
                self.sock.sendall((json.dumps(message) + '\n').encode())
                line = self.reader.readline(4097)
                if len(line) > 4096 or not line.endswith(b'\n'):
                    raise ValueError('Invalid bridge frame')
                result = json.loads(line)
                if not result.get('ok'):
                    raise ValueError('Bridge rejected request')
                return result['state']
            except (OSError, ValueError, KeyError, TypeError):
                self.close()
                raise ConnectionError('Renode bridge disconnected') from None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Do not log user data or firmware paths.

    def setup(self):
        super().setup()
        self.connection.settimeout(3)

    def send_content(self, status, data, kind='application/json; charset=utf-8'):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; connect-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def local_request(self, mutation=False):
        port = self.server.server_port
        hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
        host = self.headers.get('Host', '')
        if host not in hosts or self.headers.get('Sec-Fetch-Site', '') in ('cross-site', 'same-site'):
            self.send_content(403, {'error': 'Local same-origin requests only'})
            return False
        origin = self.headers.get('Origin')
        if origin is not None and origin != f'http://{host}':
            self.send_content(403, {'error': 'Origin rejected'})
            return False
        if mutation and (origin != f'http://{host}' or self.headers.get('X-Virtual-Lab') != '1'):
            self.send_content(403, {'error': 'Same-origin input required'})
            return False
        return True

    def do_GET(self):
        if not self.local_request():
            return
        if self.path == '/api/state':
            self.bridge_request({'op': 'state'})
            return
        assets = {'/static/img/fan.png': ('static/img/fan.png', 'image/png'),
                  '/static/img/stm32f446re.png': ('static/img/stm32f446re.png', 'image/png'),
                  '/': ('index.html', 'text/html; charset=utf-8'),
                  '/static/app.js': ('static/app.js', 'text/javascript; charset=utf-8'),
                  '/static/style.css': ('static/style.css', 'text/css; charset=utf-8')}
        if self.path not in assets:
            self.send_content(404, {'error': 'Not found'})
            return
        path, kind = assets[self.path]
        self.send_content(200, (ROOT / path).read_bytes(), kind)

    def do_POST(self):
        if not self.local_request(mutation=True):
            return
        if self.path != '/api/input':
            self.send_content(404, {'error': 'Not found'})
            return
        try:
            if self.headers.get('Transfer-Encoding') or self.headers.get('Content-Type') != 'application/json':
                raise ValueError()
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 512:
                raise ValueError()
            data = json.loads(self.rfile.read(length))
            signal, value = validate_input(data)
        except (ValueError, TypeError, UnicodeError):
            self.send_content(400, {'error': 'Invalid input: AnalogInput0 0..4095 or PSW/TSW boolean'})
            return
        self.bridge_request({'op': 'input', 'signal': signal, 'value': value})

    def bridge_request(self, message):
        try:
            state = self.server.bridge.request(message)
            self.send_content(200, {'connected': True, 'state': state})
        except ConnectionError:
            self.send_content(503, {'connected': False, 'error': 'Start Renode with run-gui.resc'})


def make_server(port=8001, bridge_port=4567):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    server.bridge = BridgeClient(bridge_port)
    return server


def main():
    port = int(os.environ.get('VLAB_HTTP_PORT', '8001'))
    bridge_port = int(os.environ.get('VLAB_BRIDGE_PORT', '4567'))
    if not all(1024 <= p <= 65535 for p in (port, bridge_port)):
        raise SystemExit('Ports must be in 1024..65535')
    server = make_server(port, bridge_port)
    print(f'Virtual Lab: http://127.0.0.1:{port} (local use only)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.bridge.close()


if __name__ == '__main__':
    main()
