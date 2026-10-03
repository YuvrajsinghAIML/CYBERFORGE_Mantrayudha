# NovaMart System Limitations & Safeguards

## 1. Clarification Thresholds
- When an entity reference (e.g. *"my laptop"*) matches more than one order in the customer's purchase history, the system never silently guesses the first match. It halts and issues an **ASK** move listing the candidate orders.
- Unauthenticated or cross-customer order queries are blocked immediately with zero private data exposure.

## 2. Policy Boundaries
- Return window calculations are strictly arithmetic: `(current_date - order_date).days <= policy.return_window_days`.
- Non-returnable categories (e.g., hygiene, perishables) are strictly enforced even if within the return window.
- Refunds over authorized limits (₹10,000 without manager approval) require automatic escalation.

## 3. Mandatory Escalations
The system deterministically transitions to **ESCALATE** for:
- Physical safety risks (battery fire, electric shock, smoke, injury).
- Legal actions (lawyer notices, consumer court summons).
- Suspended or high-risk accounts attempting financial transactions.
