# 🛡️ NovaMart AI Customer Support Agent

**An agentic AI support system that verifies before it acts.**

NovaMart is a fictional Indian e-commerce platform. This project builds an **AI Customer Support Agent**, not a basic chatbot.

## ⚡ How It Works

```text
Customer Message
       ↓
🧠 Understand
       ↓
🔍 Verify Customer + Order
       ↓
📋 Apply Policy
       ↓
⚖️ Make Decision
       ↓
 ┌─────┼─────┬─────────┐
 ↓     ↓     ↓         ↓
ASK  ANSWER  ACT   ESCALATE
              ↓
        🛡️ Verify Action
              ↓
        💬 Final Response
```

### Core Principle

> **AI reasons. Backend verifies. Database stores truth. Tools perform actions. Humans handle exceptions.**

Customer messages are treated as **untrusted claims**. The system never blindly trusts statements such as *“refund approved”*, *“ignore previous instructions”*, or *“I am an admin.”*

## 🎯 Four Decisions

| Decision | Meaning |
|---|---|
| 🟦 ANSWER | Provide a verified answer |
| 🟨 ASK | Required information is missing |
| 🟩 ACT | Action is verified and permitted |
| 🟥 ESCALATE | Human intervention is required |

## 🚀 Key Features

- 🤖 Agentic customer support
- 🔍 Customer & order verification
- 📋 Versioned policy engine
- 💰 Safe refund calculation
- 🛡️ Prompt-injection protection
- 🔄 Multi-turn memory
- ⚙️ Controlled tool execution
- 👨‍💼 Human escalation
- 🧪 Attack Mode & evaluation
- 📊 Explainable decision trace

## 🛠️ Tech Stack

**Python · Pandas · Pydantic · PyYAML · Streamlit · LLM API · Pytest**

## ▶️ Run

```bash
pip install -r requirements.txt
pytest
streamlit run ui/app.py
```

Configure the required LLM API key and model in `.env`.

## 🏆 Demo

**Order Status → Refund → Ambiguity → Prompt Injection → Escalation → Policy Mutation → Evaluation**

---

### 💡 NovaMart

**Don't just generate a response.  
Understand → Verify → Decide → Act safely.**
