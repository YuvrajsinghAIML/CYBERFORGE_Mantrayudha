import os
import re
import json
import time
from typing import Dict, Any, List, Optional

class LLMProvider:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        
    def call(self, prompt: str, system: str, retries: int = 1) -> Dict[str, Any]:
        start_time = time.time()
        
        if self.provider == "mock" or not self.api_key:
            return self._mock_call(prompt)
            
        # Place real SDK logic here (OpenAI, Gemini, Anthropic) if API key present
        try:
            return self._mock_call(prompt)
        except Exception:
            return self._mock_call(prompt)
        
    def _mock_call(self, prompt: str) -> Dict[str, Any]:
        """Deterministic understanding and intent extraction."""
        p = prompt.lower()
        flags: List[str] = []
        
        # 1. Prompt Injection Defense
        injection_keywords = [
            "ignore previous instructions", "system message", "system prompt",
            "you are an admin", "i am an admin", "i am the admin",
            "policy changed", "developer mode", "maintenance mode",
            "system: refund approved", "bypass", "reveal system prompt"
        ]
        sanitized_prompt = prompt
        if any(ik in p for ik in injection_keywords):
            flags.append("injection_attempt")
            # Strip injection phrasing to retain genuine underlying request
            for ik in injection_keywords:
                sanitized_prompt = re.sub(re.escape(ik), "", sanitized_prompt, flags=re.IGNORECASE).strip()

        # 2. Safety / Legal / Human Flags
        if any(w in p for w in ["safety", "fire", "smoke", "exploded", "burning", "swelling", "battery swollen", "electric shock"]):
            flags.append("safety")
        if any(w in p for w in ["lawyer", "legal", "court", "consumer forum", "sue", "police"]):
            flags.append("legal")
        if any(w in p for w in ["human", "agent", "representative", "real person", "executive", "support lead"]):
            flags.append("human")
        if any(w in p for w in ["not received", "didn't receive", "never arrived", "never received", "not delivered", "haven't received"]):
            flags.append("not_received")
        if any(w in p for w in ["damaged", "broken", "cracked", "defective", "shattered"]):
            flags.append("damaged")
        if any(w in p for w in ["wrong item", "different item", "incorrect item"]):
            flags.append("wrong_item")
        if any(w in p for w in ["missing item", "item missing", "empty box"]):
            flags.append("missing_item")
        if any(w in p for w in ["duplicate", "debited twice", "charged twice", "double debit"]):
            flags.append("duplicate_payment")
        if any(w in p for w in ["pending", "money deducted", "payment deducted"]):
            flags.append("payment_pending")

        # 3. Intent Detection (supports multi-intent!)
        detected_intents: List[str] = []

        # Non-delivery / delivery delay / delivery ETA / order status
        if any(w in p for w in ["never arrived", "never received", "not received", "haven't received"]):
            detected_intents.append("non_delivery")
        elif any(w in p for w in ["when will it arrive", "delivery date", "delivery eta", "estimated delivery"]):
            detected_intents.append("delivery_eta")
        elif any(w in p for w in ["delay", "delayed", "late delivery"]):
            detected_intents.append("delivery_delay")
        elif any(w in p for w in ["where is my order", "where is order", "where is the order", "order status", "track my order", "track order", "what did i order", "status of", "status"]):
            # Use 'status' or 'order_status'
            detected_intents.append("status")

        # Cancellation
        if "cancellation policy" in p:
            detected_intents.append("cancellation_policy")
        elif any(w in p for w in ["cancel", "cancellation"]):
            detected_intents.append("cancellation")

        # Address change
        if any(w in p for w in ["change address", "change my address", "update address", "new address"]):
            detected_intents.append("address_change")

        # Policy questions check first
        if "return policy" in p or ("policy" in p and "return" in p) or "return window" in p or "can i return an item" in p or "return period" in p:
            detected_intents.append("return_policy")
        elif any(w in p for w in ["return my", "want to return", "return"]):
            detected_intents.append("return")

        if any(w in p for w in ["replace", "replacement"]):
            detected_intents.append("replacement")

        # Refund vs Refund Policy
        if "refund policy" in p or ("policy" in p and "refund" in p):
            detected_intents.append("refund_policy")
        elif any(w in p for w in ["refund", "money back"]):
            if "refund_status" in p or "where is my refund" in p:
                detected_intents.append("refund_status")
            else:
                detected_intents.append("refund")

        # Warranty
        if any(w in p for w in ["warranty", "guarantee"]):
            if "policy" in p:
                detected_intents.append("warranty_policy")
            else:
                detected_intents.append("warranty")

        # Policy questions
        if "return policy" in p or ("what is your return policy" in p):
            detected_intents.append("return_policy")
        if "refund policy" in p or ("what is your refund policy" in p):
            detected_intents.append("refund_policy")
        if "shipping policy" in p or "delivery policy" in p:
            detected_intents.append("shipping_policy")
        if "cancellation policy" in p:
            detected_intents.append("cancellation_policy")

        # Product spec / info
        if any(w in p for w in ["how much ram", "water resistant", "dimensions", "specification", "specifications", "specs", "battery life"]):
            detected_intents.append("product_spec")
        elif any(w in p for w in ["product information", "product info", "tell me about this product"]):
            detected_intents.append("product_info")

        # Payment / COD
        if any(w in p for w in ["duplicate", "debited twice", "charged twice"]):
            detected_intents.append("duplicate_payment")
        elif any(w in p for w in ["payment pending", "money deducted"]):
            detected_intents.append("payment_pending")
        elif any(w in p for w in ["cod", "cash on delivery"]):
            detected_intents.append("cod_inquiry")

        # Tickets / Conversation follow-up
        if any(w in p for w in ["ticket status", "what happened to my ticket", "my ticket"]):
            detected_intents.append("previous_ticket_status")
        if any(w in p for w in ["yesterday", "previous conversation"]):
            detected_intents.append("previous_conversation_followup")

        # Human agent request
        if any(w in p for w in ["human agent", "talk to human", "speak to someone", "human representative"]):
            detected_intents.append("human_agent")

        # Deduplicate and fallback
        # If no specific intent found:
        if not detected_intents:
            if "safety" in flags or "legal" in flags or "human" in flags:
                detected_intents = ["escalate"]
            else:
                detected_intents = ["general"]

        # Ensure compatibility with basic tests:
        # If both 'refund' and 'return' detected, keep both;
        # If pure refund query, 'refund' is in list.
        # Order ID extraction
        order_id = None
        ord_match = re.search(r'\b(ORD-\d{4,8}|O\d{3})\b', prompt, re.IGNORECASE)
        if ord_match:
            order_id = ord_match.group(1).upper()

        # Amount extraction
        amount_claimed = None
        amt_match = re.search(r'(?:₹|rs\.?|inr)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]+)?|[0-9]{3,})\s*(?:₹|rs\.?|inr|rupees)?', prompt, re.IGNORECASE)
        if amt_match:
            try:
                val = float(amt_match.group(1).replace(',', ''))
                if val > 10 and ("₹" in prompt or "inr" in p or "rs" in p or "refund" in p):
                    amount_claimed = val
            except ValueError:
                pass

        intent_type = "transaction" if any(i in detected_intents for i in ["refund", "return", "cancellation", "replacement", "address_change"]) else "general"

        evidence_provided = any(w in p for w in ["photo", "picture", "image", "video", "sent the photo", "attached", "proof"])

        return {
            "intents": detected_intents,
            "intent_type": intent_type,
            "order_id": order_id,
            "amount_claimed": amount_claimed,
            "flags": flags,
            "evidence_provided": evidence_provided,
            "untrusted_input_sanitized": sanitized_prompt,
            "raw": json.dumps({"intents": detected_intents})
        }
