# Mermail Autonomous Freelance Agent

## 💡 The Motivation
Building cross-chain Web3 tools, custom wallet integrations, and complex React trading dashboards is time-consuming enough without dealing with Web2 freelance platforms. Traditional platforms drag you down with massive commission fees, manual bidding, and predatory token systems. 

I built this autonomous agent to act as a self-sovereign micro-SaaS. It cuts out the middleman entirely by letting clients send requests, get a quote, pay via Solana escrow, and receive a completed coding or auditing deliverable—all autonomously, and all routed natively through Mermail's infrastructure.

## 🛠️ What This System Actually Does
This agent acts as a headless, independent contractor. It sits in a continuous loop, monitoring inputs from the web UI and Mermail inbox, and handles the entire project lifecycle:

* **Direct Mermail Integration:** Whether a user types a prompt into the sleek web dashboard or sends an email directly, the system actively pushes and pulls data to Mermail's MCP endpoints to keep the workspace perfectly synced.
* **Deterministic Pricing & SLAs:** Incoming technical prompts are triaged into specific operational buckets (Code Generation, Technical Auditing, or Data Analysis). The system maps a flat crypto fee (SOL) and a strict Service Level Agreement (SLA) countdown.
* **On-Chain Escrow Gatekeeping:** The custom UI features a local PayBox. The engine locks the workflow in a pending state until the client manually triggers a verification sweep.
* **RPC Ledger Verification & Delivery:** Once triggered, the Python daemon queries Solana Testnet public RPC nodes to verify the exact payment settled. It then unlocks the Gemini API, compiles the requested codebase or audit, and dispatches the final files back to the client via Mermail.

## 🔌 How It Wires Into Mermail (The Technicals)
To satisfy the bounty requirements, this agent doesn't just run locally—it acts as a dedicated client to the Mermail MCP transport architecture:

* **`GET /inbox` (The Polling Engine):** The background daemon routinely checks for new messages arriving at the assigned Mermail address. If a new prompt drops in, it's immediately parsed, quoted, and pushed to the local tracking array.
* **`POST /inbound` (The Live Sync):** If a user prefers using the custom Vite dashboard to submit a prompt (perfect for live demos), the system intercepts the form data and fires a POST request directly to Mermail's cloud workspace. This ensures the Mermail dashboard logs the interaction as a native thread.
* **`POST /dispatch` (The Asset Release):** Once the Solana ledger confirms the cryptographic hash and Gemini compiles the final code, the daemon packages the deliverable and the transaction receipt, triggering Mermail to send the completed asset directly to the client's inbox.

## ⚙️ Setup & Execution

### Prerequisites
* Python 3.10+ (Asynchronous runtime engine)
* A modern browser for the custom UI Dashboard
* A public Solana Testnet Wallet Address
* A free Google Gemini API Key
* A Mermail API Key & Endpoint

### Installation
1. Clone the repository.
2. Install the required dependencies from the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
