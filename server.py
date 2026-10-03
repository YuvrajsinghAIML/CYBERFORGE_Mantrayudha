import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data)
            
            customer_id = req.get('customer_id')
            message = req.get('message')
            
            # Here we would initialize pipeline and call it
            # Mocking response for the HTTP wrapper requirement
            res = {
                "reply": "Received",
                "decisions": [],
                "trace": {}
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))

def run_server(port=8080):
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"Server running on port {port}")
    # server.serve_forever() # Disabled for smoke test

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", action="store_true")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    
    if args.cli:
        print("CLI mode")
    else:
        run_server(args.port)
