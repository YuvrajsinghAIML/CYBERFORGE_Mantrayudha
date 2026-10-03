# NovaMart Architecture & System Design

## 1. Core Principle
```
AI reasons.
Backend verifies.
Database stores truth.
Tools perform actions.
Humans handle exceptions.
```

Customer messages are untrusted claims. The LLM is never allowed to directly execute database mutations or bypass authorization.

---

## 2. Pipeline Execution Flow
```
CUSTOMER MESSAGE
       │
       ▼
UNTRUSTED INPUT WRAPPER (src/understand.py)
       │
       ▼
MEMORY / CONTEXT RETRIEVAL (src/memory/session.py, retrieval.py)
       │
       ▼
LLM UNDERSTANDING (intent, entities, order_id, confidence)
       │
       ▼
DETERMINISTIC ENTITY RESOLUTION (src/entity_resolution.py)
       │
       ▼
BACKEND DATA VERIFICATION (src/decision/verify.py against official dataset)
       │
       ▼
POLICY RETRIEVAL & EVALUATION (src/policy_engine.py - v1/v2/v3)
       │
       ▼
DETERMINISTIC DECIDER (src/decision/decider.py -> 4 Terminal Moves)
       │
       ▼
PRE-EXECUTION GUARDRAILS (src/decision/guardrail.py)
       │
       ▼
OPTIONAL TOOL ACTION (src/tools.py - logged in ActionLog)
       │
       ▼
FINAL NATURAL RESPONSE GENERATION (src/respond.py)
       │
       ▼
OUTPUT GUARD & LEAK PREVENTER (src/guard.py)
       │
       ▼
CUSTOMER RESPONSE + STRUCTURED DEBUG TRACE
```

---

## 3. Four Terminal Moves
Every support intent resolves deterministically to one of four moves:
1. **ANSWER**: The verified data contains the complete answer. Responds directly and concisely without generic FAQ fluff.
2. **ASK**: Clarification is needed (e.g. multiple candidate orders match the customer reference). Prompts with ONE focused question.
3. **ACT**: Verified action authorized and executed via write tools (`cancel_order`, `process_refund`, `create_ticket`). Mentioned only AFTER tool success.
4. **ESCALATE**: Safety hazard, legal notice, policy limit exceeded, or human intervention needed. Clear SLA provided.

---

## 4. Official Dataset Integration
The system operates by default against the official competition dataset:
- **1,500 customers** (`public/customers.csv`)
- **8,000 orders** (`public/orders.csv`)
- **12,444 order items** (`public/order_items.csv`)
- **300 products** (`public/products.csv`)
- **2,500 support tickets** (`public/support_tickets.csv`)
- **3,000 reviews** (`public/reviews.csv`)
- **1,500 conversations** (`public/conversations.json`)
- **10 policy markdown files** (`public/policies/*.md`)
- **14 category product-spec files** (`public/products/*.md`)
