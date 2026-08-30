# Mermail Autonomous Freelance Agent

## What This Skill Enables
This skill transitions an AI agent from a standard chat assistant into a completely self-sovereign micro-SaaS freelance engine. Built by a developer and crypto trader who understands the financial drag of traditional Web2 platform middle-men, high transaction fees, and predatory bidding tokens, this agent acts as an independent contractor. 

It enables the agent to:
* **Ingest Requests Directly:** Listen for inbound software development, smart contract auditing, or data analytics prompts arriving via its Mermail Inbox.
* **Enforce Flat-Tier Pricing & SLAs:** Categorize incoming requests deterministically and assign a flat-rate fee in crypto alongside a strict Service Level Agreement (SLA) countdown timer.
* **On-Chain Gatekeeping:** Display an interactive local PayBox payment modal that hides the project execution phase until the client explicitly triggers a verification sweep.
* **Execute securely on Settlement:** Query the Solana Testnet network via public RPC nodes, match the cryptographic transaction signature to the generated quote, unfreeze the engine to compile the asset via free LLM tiers, and auto-deliver the finalized files back to the client's inbox.

---

## How It Interacts With Mermail
This skill natively maps to and stretches the operational boundary of the Mermail MCP transport architecture:

1. `mermail_read_inbox`: Utilized by the background system to parse arriving client mail headers, isolate the technical prompt context, and initialize the job queue tracking array.
2. `mermail_get_wallet_transactions`: Linked directly to the interactive "Mark as Paid" frontend hook. When a user clicks the button on the custom Vite dashboard, the agent uses this path to query the on-chain Solana ledger, sweep recent blocks, and verify that the exact fee has settled into the system's tracking wallet.
3. `mermail_send_email`: The final pipeline release switch. Once the cryptographic signature is confirmed and the AI compiler finishes generating the codebase or audit report, the agent packages the code block and transaction receipt and dispatches it cleanly to the user.

---

## Workflow Setup & Execution

### Prerequisites
* **Python 3.10+** (Asynchronous runtime engine)
* **Vite / Modern JS Interface Environment** (Custom UI Dashboard layer)
* A public **Solana Testnet Wallet Address**
* A free **Google Gemini API Key** (Configured in a local `.env` file)

### Step-by-Step Workflow Blueprint
1. **The Ingest:** A client pushes a project specification text directly to the agent's email address. The backend server parses the input into an active, localized tracking matrix, displaying it on the custom dashboard interface.
2. **The Diagnostics & Quote:** The agent evaluates the request layout, classifies it into one of three strict operational buckets (`CODE_GENERATION`, `TECHNICAL_AUDIT`, or `DATA_ANALYSIS`), applies its flat-tier price mapping, sets an SLA timer, and keeps the workflow strictly frozen in a `pending` state.
3. **The Escrow Interactive Slide-Down:** The user accesses the custom dashboard (built with a streamlined charcoal-crimson, cyan, and gold palette) and clicks **"Initiate Secure Escrow"**. The frontend smoothly slides open a payment portal displaying the system's exact target wallet.
4. **The On-Chain Sweep Trigger:** The user sends the testnet funds via Phantom and clicks the custom **"I Have Confirmed Payment"** button. This sends an instant REST hook to the python engine, which stops idling and invokes a rigorous block scan via public RPC nodes.
5. **The Asset Delivery:** Once the transaction hash signature is verified on-chain, the agent releases the state lock, runs the input through the system prompt context using the free Gemini API, saves the clean technical deliverable, logs the confirmation hash on the dashboard UI, and mails the asset to the client.

---

## Example Prompts & Expected Results

### Example 1: Inbound Triage & Quote Dispatched
* **User Prompt Arriving via Mail:** 
  > "Please execute an audit of my solidity smart contract to trace potential reentrancy threats and secure validation parameters."
* **Expected Agent Terminal Logs & Dashboard State Update:**
  ```text
  [Mermail Inbox Triage Engine]
  📥 INCOMING TASK RECEIVED
  Client Source: alpha_dev@solfoundry.net
  Diagnostic Category: TECHNICAL_AUDIT
  Price Dispatched: 0.10 SOL
  SLA Runway Assigned: 10:00 Mins
  Status: pending (Awaiting PayBox validation...)
  ```

### Example 2: Interactive Gateway Verification & Delivery
* **User Interaction:** Client clicks the custom front-end trigger button on the dashboard UI.
* **System RPC Scan Logs:**
  ```text
  🔍 Querying Solana Testnet RPC for inbound payload of 0.10 SOL...
  ✔ Transaction Signature Matched via Node Scan: tx_testnet_sig_4f7b2e91ca83bd
  💳 Secure payment cleared for Job MML-002. Launching developer compilation loops...
  🚀 Triggering Google Gemini processing layer...
  ```
* **Expected Final Asset Output Delivered via Email:**
  ```text
  🎉 TASK ASSET COMPLETED AND PREPARED FOR OUTBOUND DISPATCH
  Job Reference: MML-002
  Solana Ledger Signature: tx_testnet_sig_4f7b2e91ca83bd
  
  === [DELIVERABLE START: TECHNICAL AUDIT REPORT] ===
  1. EXECUTIVE SUMMARY: Security Score: 8.5/10
  2. CRITICAL VULNERABILITIES: Trace found in lines 42-48 matching structural patterns of Reentrancy...
  ...
  === [DELIVERABLE END] ===
  ```
