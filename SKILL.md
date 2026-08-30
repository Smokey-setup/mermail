---
name: mermail-autonomous-freelancer
description: A micro-SaaS agent skill that allows an AI to quote prices for tasks, verify incoming USDC payments via the Mermail Agent Wallet, and deliver the completed work via the Mermail Inbox.
author: Mermail Skill Developer
version: 1.0.0
tags: [mermail, mcp, autonomous-agent, payments, crypto, micro-saas]
---

# Mermail Autonomous Freelance Agent

## What This Skill Enables
This skill transforms an AI agent from a simple assistant into a self-sovereign micro-business. It enables the agent to:
1. Receive work requests via its own Mermail Inbox.
2. Calculate and quote a dynamic USDC price based on the complexity of the task.
3. Automatically monitor its Mermail Agent Wallet for incoming payments.
4. Withhold the final deliverable until cryptographic proof of payment (the transaction hash) is verified.
5. Execute the work and deliver the final result via email.

## How It Interacts With Mermail
This skill heavily utilizes the Mermail MCP transport layer:
* **`mermail_read_inbox`**: Used to poll for incoming client requests and evaluate intent.
* **`mermail_send_email`**: Used to send quotes and final deliverables back to the client.
* **`mermail_get_wallet_transactions`**: Used to query the agent's on-chain Solana wallet to verify that the exact USDC payment amount has arrived from the client.

## Workflow Setup & Execution

### Prerequisites
- Python 3.10+
- A Mermail API Key and Agent Wallet Address.
- An Anthropic or OpenAI API Key for task execution.

### Step-by-Step Workflow
1. **The Request:** A user sends an email to the agent asking for a task (e.g., "Write a Solana liquidity scraper in Python").
2. **The Quote:** The agent evaluates the prompt, categorizes the service (e.g., `CODE_GENERATION`), and replies with a quote (e.g., 1.50 USDC) and its wallet address.
3. **The Lock:** The agent suspends execution and polls its wallet balance. It will not process the task if the user replies demanding the work for free.
4. **The Payment:** The user sends the exact USDC amount on-chain.
5. **The Delivery:** The agent detects the transaction, executes the LLM task, and emails the user the final code block alongside the transaction receipt.

## Example Prompts & Expected Results

### Example 1: Initial Work Request
**User Prompt (via Email):**
> "Can you generate a technical audit report for my smart contract based on standard reentrancy vulnerabilities?"

**Expected Agent Result (Quote Email):**
> "Hello! I have reviewed your request. Service Category: TECHNICAL_AUDIT. Required Fee: 2.50 USDC. Please send payment to [Agent Wallet Address]. Once payment is detected on-chain, I will execute the work."

### Example 2: Payment Verification & Delivery
**System Trigger:** 
> Agent detects 2.50 USDC incoming transaction on Solana mainnet.

**Expected Agent Result (Final Delivery Email):**
> "Payment Confirmed! Transaction Hash: 0x123... Amount: 2.50 USDC. 
> [DELIVERABLE START] 
> Here is your technical audit report... 
> [DELIVERABLE END]"
