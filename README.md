# Agentic AI Task Orchestrator (Tool-Using LLM with Memory & Guardrails)

Live Demo: https://agentic-genai-orchestrator.onrender.com  
API Docs (Swagger): https://agentic-genai-orchestrator.onrender.com/docs  

---

## 🚀 Overview

Agentic AI Task Orchestrator is a production-ready GenAI system that accepts high-level user tasks and autonomously plans steps, uses tools (web search, calculator, code execution), retries on failures, stores short-term memory, and returns structured results.

This project demonstrates how to build **reliable agentic systems around unreliable LLMs**, exposing them as real APIs and UIs.

---

## ✨ Key Capabilities

- 🧠 **Planning & Reasoning Loop** — Breaks tasks into steps
- 🔧 **Tool Use** — Live web search (Tavily), calculator, code execution
- ♻️ **Retries & Guardrails** — Handles tool/LLM failures gracefully
- 🗃️ **Memory** — Stores recent context across steps
- 📦 **Structured Output** — Returns JSON with result + reasoning steps
- 🌐 **Production Deployment** — FastAPI service deployed on Render
- 🧪 **Interactive UI + API Docs** — Try it via browser or curl

---

## 🏗️ Architecture

User Task
│
▼
Agent Loop (Plan → Tool → Evaluate → Retry)
│
├── Tavily Search Tool
├── Calculator Tool
└── Code Execution Tool
│
▼
Structured JSON Output (result + steps)


---

## 🛠️ Tech Stack

- Python, FastAPI  
- Groq (Open-source LLMs)  
- Tavily Search API  
- Custom agent loop  
- Render (deployment)  
- HTML UI  

---

## 📦 Example API Request

```bash
curl -X POST "https://agentic-genai-orchestrator.onrender.com/run" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Research top 3 payment gateway competitors of Razorpay in India and summarize their pricing"
  }'


