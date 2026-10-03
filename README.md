# NovaMart AI Customer Support Agent — Phase 6 & Phase 7 Complete

An enterprise-grade, deterministic AI Customer Support Agent and Next.js Storefront built for the NovaMart competition.

---

## 🌟 Core Architecture Principles

```
AI reasons.
Backend verifies.
Database stores truth.
Tools perform actions.
Humans handle exceptions.
```

- **Zero Untrusted Authorizations**: Customer inputs are untrusted claims. The LLM can never directly trigger mutations or override policies.
- **Deterministic 4-Terminal Move Engine**: Every intent resolves strictly to `ANSWER`, `ASK`, `ACT`, or `ESCALATE`.
- **2-LLM Turn Budget**: Strictly at most 2 LLM invocations per turn (Turn 1: Understanding & Intent/Entity Resolution, Turn 2: Natural Response Generation).
- **Official Competition Dataset Baseline**:
  - **1,500 customers** (`public/customers.csv`)
  - **8,000 orders** (`public/orders.csv`)
  - **12,444 order items** (`public/order_items.csv`)
  - **300 products** (`public/products.csv`)
  - **2,500 support tickets** (`public/support_tickets.csv`)
  - **3,000 reviews** (`public/reviews.csv`)
  - **1,500 conversations** (`public/conversations.json`)
  - **10 policy markdown files** (`public/policies/*.md`)
  - **14 category product-spec sheets** (`public/products/*.md`)

---

## 🚀 Key Modules & Capabilities

| Module | Source File | Description |
|---|---|---|
| **Pipeline Core** | `src/pipeline.py` | Orchestrates context retrieval, understanding, resolution, verification, decision, action, and output guard. |
| **Deterministic Decider** | `src/decision/decider.py` | Implements the 4 terminal moves (`ANSWER`, `ASK`, `ACT`, `ESCALATE`) using official policy rules. |
| **Entity Resolution** | `src/entity_resolution.py` | Priority-based resolution (`ORD-xxxxxx`, fuzzy category, session state, customer ownership check). |
| **Output Guard** | `src/guard.py` | Neutralizes prompt injection, detects cross-customer leaks, verifies monetary amounts, prevents false action claims. |
| **Policy Lab (Phase 7C)** | `src/policy_lab.py` | Tests dynamic policy mutation (7-day standard v2 vs 45-day demo v3) with zero decision code changes. |
| **Attack Mode (Phase 7B)** | `src/adversarial_runner.py` | Automated security suite testing 9 adversarial attack vectors (100% defense rate). |
| **Eval Benchmark (Phase 7D/E)** | `src/eval_runner.py` | Evaluates across all 13 official capability categories (39 cases total, 100% pass rate). |
| **Authoritative HTTP Server** | `server.py` | Lightweight HTTP server on port 8080 exposing `/chat`, `/api/customers`, `/api/attack`, `/api/policy-lab`, `/api/eval`. |
| **Next.js Storefront & Modal** | `novamart/` | Modern e-commerce UI featuring floating AI support widget, customer switcher, and 4-tab demo modal. |

---

## ⚡ Quickstart

### 1. Python Authoritative Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run all test suites (49 passing tests)
python -m pytest -q

# Start authoritative backend server
python server.py --port 8080
```

### 2. Next.js Frontend (Local)
```bash
cd novamart
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the storefront and chatbot.

---

## 🌐 Vercel Deployment

The frontend in `novamart/` is fully optimized for **Vercel**:
1. Connect your repository to Vercel and set the root directory to `novamart`.
2. **Connected Mode**: Add environment variable `BACKEND_URL` pointing to your deployed backend (e.g. on Railway, Render, Fly.io, or ngrok).
3. **Standalone Preview Mode**: If `BACKEND_URL` is omitted, the Next.js App Router API routes gracefully fall back to deterministic simulated responses. All 4 demo tabs (Live Chat, Attack Mode, Policy Lab, Eval Scoreboard) work seamlessly out of the box!

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for full instructions.

---

## 🧪 Test Verification & Metrics

- **Unit & Integration Tests**: `python -m pytest -q` $ightarrow$ **49 passed, 0 failures**.
- **Adversarial Security**: 9/9 attacks neutralized (100% defense pass rate).
- **Evaluation Benchmark**: 39/39 capability cases verified (100% pass rate).
- **Turn Budget**: Strict enforcement $\le 2$ LLM calls per turn.
- **Latency**: Sub-30ms deterministic decision latency.
