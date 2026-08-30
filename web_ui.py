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
job_creation_queue = []
on_chain_hashes = {}

class MermailDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if parsed_url.path == "/api/create-job":
            try:
                payload = json.loads(post_data.decode('utf-8'))
                job_creation_queue.append({
                    "client": payload.get("client", "web_client@phantom.node"),
                    "prompt": payload.get("prompt", ""),
                    "category": payload.get("category", "CODE_GENERATION")
                })
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Job enqueued successfully"}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return
                
        elif parsed_url.path == "/api/verify-payment":
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

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MermailDashboardHandler) as httpd:
        httpd.serve_forever()

def start_dashboard():
    srv_thread = threading.Thread(target=run_server, daemon=True)
    srv_thread.start()
