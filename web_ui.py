import logging
import os

class WebDashboardExporter:
    """Writes a live, auto-refreshing HTML dashboard for users who prefer web UI."""
    FILE_NAME = "web_dashboard.html"

    @classmethod
    def update_dashboard(cls, jobs_iterable, agent_wallet: str):
        rows_html = ""
        # Get the last 10 jobs
        recent_jobs = list(jobs_iterable)[-10:]
        
        for job in reversed(recent_jobs):
            tx = job.payment_tx_hash[:15] + "..." if job.payment_tx_hash else "PENDING"
            status_color = "#eab308" # yellow
            
            # Use string matching to avoid circular imports with agent.py enums
            if job.status.value == "DELIVERED":
                status_color = "#22c55e" # green
            elif job.status.value == "PAYMENT_VERIFIED":
                status_color = "#06b6d4" # cyan

            rows_html += f"""
            <tr style="border-bottom: 1px solid #333;">
                <td style="padding: 12px; color: #38bdf8;">{job.job_id[:8]}</td>
                <td style="padding: 12px; color: #e879f9;">{job.client_email}</td>
                <td style="padding: 12px; color: #4ade80;">{job.category.value}</td>
                <td style="padding: 12px; color: #facc15;">${job.quoted_price_usdc:.2f}</td>
                <td style="padding: 12px; color: {status_color}; font-weight: bold;">{job.status.value}</td>
                <td style="padding: 12px; color: #60a5fa;">{tx}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="2"> <!-- Auto-refreshes every 2 seconds -->
            <title>Mermail Agent Live Dashboard</title>
            <style>
                body {{ font-family: 'Courier New', monospace; background-color: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }}
                h1 {{ color: #ffffff; }}
                .header-panel {{ background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }}
                .highlight {{ color: #fbbf24; font-weight: bold; }}
                .status-blink {{ color: #4ade80; animation: blinker 1.5s linear infinite; font-weight: bold; }}
                @keyframes blinker {{ 50% {{ opacity: 0; }} }}
                table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }}
                th {{ background: #334155; color: #cbd5e1; text-align: left; padding: 12px; }}
            </style>
        </head>
        <body>
            <h1>Mermail Agent Dashboard</h1>
            <div class="header-panel">
                <p>MERMAIL AGENT WALLET: <span class="highlight">{agent_wallet}</span></p>
                <p>SYSTEM STATUS: <span class="status-blink">● LISTENING FOR INCOMING INBOX & PAYMENT EVENTS</span></p>
            </div>
            <table>
                <thead>
                    <tr><th>Job ID</th><th>Client</th><th>Category</th><th>Quote (USDC)</th><th>Status</th><th>Tx Hash</th></tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </body>
        </html>
        """
        try:
            with open(cls.FILE_NAME, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            logging.error(f"Failed to update web dashboard: {str(e)}")
