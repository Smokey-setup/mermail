import http.server
import socketserver
import json
import os
import threading
import time
from urllib.parse import urlparse, parse_qs

PORT = 8000
STATE_FILE = "state.json"

payment_trigger_queue = []
on_chain_hashes = {}

class MermailDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Suppresses default HTTP logging to keep your rich terminal interface clean."""
        return

    def end_headers(self):
        """Injects clean CORS headers so your Vite frontend can communicate without browser blocking."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        """Handles browser pre-flight safety checks gracefully."""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                fallback = {"agent_wallet": "Configuring...", "jobs": []}
                self.wfile.write(json.dumps(fallback).encode('utf-8'))
                
        elif parsed_url.path == "/api/view-deliverable":
            query_params = parse_qs(parsed_url.query)
            job_id = query_params.get("id", [None])[0]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            asset_path = f"deliverable_{job_id}.txt" if job_id else ""
            if asset_path and os.path.exists(asset_path):
                with open(asset_path, "r") as f:
                    self.wfile.write(json.dumps({"status": "success", "content": f.read()}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"status": "error", "message": "Asset compilation processing..."}).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/api/verify-payment":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                job_id = payload.get("id")
                client_wallet = payload.get("client_wallet", "Unknown")
                
                if job_id:
                    payment_trigger_queue.append({"id": job_id, "client_wallet": client_wallet})
                    
                    timeout = 10
                    while timeout > 0 and job_id not in on_chain_hashes:
                        time.sleep(0.5)
                        timeout -= 0.5
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    
                    if job_id in on_chain_hashes:
                        response_body = {"status": "success", "tx_hash": on_chain_hashes[job_id]}
                    else:
                        response_body = {"status": "scanning", "message": "Transaction routing on Solana network..."}
                        
                    self.wfile.write(json.dumps(response_body).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return

            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Invalid tracking parameters"}).encode('utf-8'))

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MermailDashboardHandler) as httpd:
        httpd.serve_forever()

def start_dashboard():
    """Launches the UI server in an independent background thread to keep execution smooth."""
    srv_thread = threading.Thread(target=run_server, daemon=True)
    srv_thread.start()
