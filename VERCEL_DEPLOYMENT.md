# NovaMart Frontend Vercel Deployment & Chatbot Integration Guide

This guide explains how the NovaMart Next.js frontend connects to the authoritative Python AI Support Agent when deployed on **Vercel**.

---

## 🚀 Architecture Overview

```
                      ┌──────────────────────────────────────────────┐
                      │             Vercel Cloud Edge                │
                      │                                              │
                      │   Next.js 16 Storefront UI (novamart/app)    │
                      │                      │                       │
                      │             Floating AI Widget               │
                      │   [Chat | Attack Mode | Policy Lab | Eval]   │
                      │                      │                       │
                      │            App Router API Routes             │
                      │        (/api/chat, /api/attack, etc.)        │
                      └──────────────────────┬───────────────────────┘
                                             │
               ┌─────────────────────────────┴────────────────────────────┐
               ▼                                                          ▼
  [MODE 1: Connected Backend]                               [MODE 2: Standalone Vercel]
  Proxy to Authoritative Python Backend                     Zero-Config Serverless Fallback
  (Railway / Render / ngrok / Fly.io)                       (Deterministic mock pipeline)
  • Real 1,500 Customer Dataset                             • Exact schema matching
  • Exact Policy v1/v2 Engine                               • 100% Interactive Hackathon Demo
  • Live Adversarial Attack Runner                          • Zero external dependencies
```

---

## 🛠️ Deployment Instructions on Vercel

### Step 1: Deploy to Vercel
1. Push this repository to GitHub or GitLab.
2. In the Vercel Dashboard, click **New Project** and import the repository.
3. Configure the **Root Directory**:
   - Set **Root Directory** to `novamart`.
4. Click **Deploy**. Vercel will build the Next.js application cleanly (`npm run build`).

---

## 🔗 Connecting the Chatbot to the Python Backend

### Mode 1: Connected Backend (Full Official Dataset & Authoritative Decisions)

If you want Vercel to route live chats, attacks, and evaluations through the authoritative Python backend:

1. **Deploy or Expose the Python Backend (`server.py`)**:
   - **Option A (Free Cloud Hosting - Railway / Render)**:
     - Deploy the root directory with start command: `python server.py --port 8080`.
     - Your backend will get a public URL like `https://novamart-backend.up.railway.app`.
   - **Option B (Instant Local Tunnel - ngrok)**:
     - Run locally: `python server.py --port 8080`
     - Run ngrok: `ngrok http 8080`
     - Copy the forwarding URL: `https://xxxx-xx-xx.ngrok-free.app`.

2. **Add Environment Variable in Vercel**:
   - Go to **Vercel Project Dashboard** $ightarrow$ **Settings** $ightarrow$ **Environment Variables**.
   - Key: `BACKEND_URL`
   - Value: `https://novamart-backend.up.railway.app` (or your ngrok URL).
   - Save and redeploy.

3. **Verification**:
   - The Next.js API route (`/api/chat`) will now automatically proxy every query to your backend.
   - Full CORS support is already enabled in `server.py` (`Access-Control-Allow-Origin: *`).

---

### Mode 2: Standalone Vercel Preview (Zero Config Required)

If `BACKEND_URL` is omitted or the backend is offline:
- The Next.js API routes automatically detect connection status and fall back to the built-in deterministic simulation.
- **What works in Standalone Mode**:
  - Live customer switcher (`CUST-00001` Aarav Sharma, `CUST-00002` Diya Patel, `CUST-00003` Kabir Mehta [Suspended], `CUST-00004` Ananya Verma [Platinum]).
  - Interactive chat with order tracking, return window verification, and safety escalations.
  - Decision badges: `[ANSWER]`, `[ASK]`, `[ACT]`, `[ESCALATE]`.
  - Collapsible Debug Drawer with trace, policy verification, and metrics budget.
  - **Attack Mode (Phase 7B)**: 9 live adversarial test cases demonstrating 100% pass rate.
  - **Policy Lab (Phase 7C)**: Dynamic comparison between 7-day v2 policy and 45-day mutated v3 policy.
  - **Eval Scoreboard (Phase 7E)**: Comprehensive benchmark across all 13 official capability categories.

---

## 💻 Local Testing & Pair Running

To run both frontend and backend locally:

```bash
# Terminal 1: Python Authoritative Backend
python server.py --port 8080

# Terminal 2: Next.js Frontend
cd novamart
npm run dev
```

Visit `http://localhost:3000` to interact with the full demo.
