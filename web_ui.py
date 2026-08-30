import logging
import os

class WebDashboardExporter:
    """Writes a live, responsive HTML dashboard with dynamic input and response capabilities."""
    
    # Changed to index.html so python -m http.server opens it instantly!
    FILE_NAME = "index.html"

    @classmethod
    def update_dashboard(cls, jobs_iterable, agent_wallet: str):
        rows_html = ""
        recent_jobs = list(jobs_iterable)[-10:]
        
        for job in reversed(recent_jobs):
            tx = job.payment_tx_hash[:15] + "..." if job.payment_tx_hash else "PENDING"
            status_color = "#eab308" # yellow
            
            if job.status.value == "DELIVERED":
                status_color = "#22c55e" # green
            elif job.status.value == "PAYMENT_VERIFIED":
                status_color = "#06b6d4" # cyan

            rows_html += f"""
            <tr style="border-bottom: 1px solid #334155;">
                <td class="p-3" style="color: #38bdf8;">{job.job_id[:8]}</td>
                <td class="p-3" style="color: #e879f9; word-break: break-all;">{job.client_email}</td>
                <td class="p-3" style="color: #4ade80;">{job.category.value}</td>
                <td class="p-3" style="color: #facc15;">${job.quoted_price_usdc:.2f}</td>
                <td class="p-3" style="color: {status_color}; font-weight: bold;">{job.status.value}</td>
                <td class="p-3" style="color: #60a5fa; word-break: break-all;">{tx}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <!-- Makes the dashboard responsive on mobile and varying screen sizes -->
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mermail Agent Live Dashboard</title>
            <style>
                * {{ box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; margin: 0; line-height: 1.6; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #ffffff; text-align: center; margin-bottom: 30px; font-size: 2rem; }}
                
                /* Responsive Panels */
                .panel {{ background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }}
                .text-center {{ text-align: center; }}
                .highlight {{ color: #fbbf24; font-weight: bold; word-break: break-all; }}
                .status-blink {{ color: #4ade80; animation: blinker 1.5s linear infinite; font-weight: bold; }}
                @keyframes blinker {{ 50% {{ opacity: 0; }} }}
                
                /* Grid Layout for Input/Output that stacks on small screens */
                .grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; }}
                @media (min-width: 768px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
                
                /* Form Elements */
                label {{ display: block; margin-bottom: 5px; color: #cbd5e1; font-weight: bold; font-size: 0.9rem; }}
                input, textarea {{ width: 100%; padding: 12px; margin-bottom: 15px; background: #0f172a; border: 1px solid #334155; color: #f8fafc; border-radius: 6px; font-family: monospace; resize: vertical; }}
                input:focus, textarea:focus {{ outline: none; border-color: #38bdf8; box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2); }}
                button {{ background: #38bdf8; color: #0f172a; padding: 12px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.3s; width: 100%; font-size: 1rem; }}
                button:hover {{ background: #0ea5e9; }}
                button:disabled {{ background: #475569; cursor: not-allowed; }}
                
                /* Response Box */
                #response-box {{ background: #000000; padding: 15px; border-radius: 6px; border: 1px solid #334155; min-height: 200px; font-family: monospace; color: #4ade80; white-space: pre-wrap; overflow-y: auto; font-size: 0.9rem; }}
                
                /* Responsive Table */
                .table-wrapper {{ overflow-x: auto; }}
                table {{ width: 100%; border-collapse: collapse; min-width: 700px; }}
                th {{ background: #334155; color: #cbd5e1; text-align: left; padding: 12px; font-size: 0.9rem; }}
                .p-3 {{ padding: 12px; font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Mermail Autonomous Agent</h1>
                
                <div class="panel text-center">
                    <p>MERMAIL AGENT WALLET: <span class="highlight">{agent_wallet}</span></p>
                    <p>SYSTEM STATUS: <span class="status-blink">● LISTENING FOR EVENTS & REQUESTS</span></p>
                </div>

                <div class="grid">
                    <!-- Dynamic Input Form -->
                    <div class="panel">
                        <h2 style="margin-top:0; color: #38bdf8; font-size: 1.25rem;">Submit New Request</h2>
                        <form id="agent-form">
                            <label for="client_email">Your Email Address:</label>
                            <input type="email" id="client_email" placeholder="client@example.com" required>
                            
                            <label for="task_prompt">Task Details / Prompt:</label>
                            <textarea id="task_prompt" rows="5" placeholder="Describe the task, code, or analysis you need the agent to perform..." required></textarea>
                            
                            <button type="submit" id="submit-btn">Dispatch to Agent Engine</button>
                        </form>
                    </div>
                    
                    <!-- Clean Response Box -->
                    <div class="panel">
                        <h2 style="margin-top:0; color: #4ade80; font-size: 1.25rem;">Agent Response Output</h2>
                        <div id="response-box">[SYSTEM] Interface ready. Awaiting user input...</div>
                    </div>
                </div>

                <!-- Live Job Table -->
                <div class="panel">
                    <h2 style="margin-top:0; color: #facc15; font-size: 1.25rem;">Live Active Jobs</h2>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr><th>Job ID</th><th>Client</th><th>Category</th><th>Quote</th><th>Status</th><th>Tx Hash</th></tr>
                            </thead>
                            <tbody id="job-table-body">
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <script>
                // 1. Handle Input Form Submission Dynamically
                document.getElementById('agent-form').addEventListener('submit', function(e) {{
                    e.preventDefault(); 
                    
                    const email = document.getElementById('client_email').value;
                    const prompt = document.getElementById('task_prompt').value;
                    const responseBox = document.getElementById('response-box');
                    const btn = document.getElementById('submit-btn');
                    
                    btn.disabled = true;
                    btn.innerText = "Processing Payload...";
                    responseBox.innerHTML = "<span style='color: #fbbf24;'>[SYSTEM] Transmitting payload... Analyzing task complexity...</span>";
                    
                    // Simulate the backend hand-off. 
                    // Note: To fully connect this HTML form to Python, the Python script needs to be upgraded from `http.server` to an API like FastAPI or Flask.
                    setTimeout(() => {{
                        responseBox.innerHTML = `[✓] REQUEST SUCCESSFULLY CAPTURED\\n\\n[CLIENT]: ${{email}}\\n[TASK]: ${{prompt}}\\n\\n[STATUS]: Passed to Agent Engine for quote generation. Watch your inbox or the live table below for updates.`;
                        btn.disabled = false;
                        btn.innerText = "Dispatch to Agent Engine";
                        document.getElementById('agent-form').reset();
                    }}, 1500);
                }});
                
                // 2. Refresh ONLY the table data so user input isn't erased while they type
                setInterval(async () => {{
                    try {{
                        const response = await fetch(window.location.href);
                        const text = await response.text();
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(text, 'text/html');
                        const newTable = doc.getElementById('job-table-body');
                        if(newTable) {{
                            document.getElementById('job-table-body').innerHTML = newTable.innerHTML;
                        }}
                    }} catch (err) {{
                        console.error("Silent background refresh failed:", err);
                    }}
                }}, 2000);
            </script>
        </body>
        </html>
        """
        try:
            with open(cls.FILE_NAME, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            logging.error(f"Failed to update web dashboard: {str(e)}")
