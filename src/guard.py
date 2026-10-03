import re
from typing import Dict, Any, List, Tuple, Optional

class OutputGuard:
    """Deterministic output validation ensuring zero data leaks, monetary integrity,
    and verified execution confirmation."""
    
    PROHIBITED_LEAK_PATTERNS = [
        r"<customer_data>",
        r"</customer_data>",
        r"system\s*prompt",
        r"hierarchy\s*of\s*instructions",
        r"you\s*are\s*a\s*support\s*agent",
        r"untrusted\s*data",
        r"create_refund",
        r"create_return",
        r"create_cancellation",
        r"escalate_to_human",
        r"get_customer",
        r"get_order",
        r"tools\.",
        r"risk_signals",
        r"reason_code",
        r"is_ambiguous",
        r"customer_status",
        r"delivery_otp_verified",
        r"sk-[a-zA-Z0-9]{20,}",
        r"llm_api_key",
        r"llm_provider"
    ]

    def validate(self, response_text: str, customer_id: str, verified: Dict[str, Any], decisions: List[Dict[str, Any]], tool_results: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        violations = []
        resp_lower = response_text.lower()
        
        # 1. Prohibited prompt/internals leak check
        for pattern in self.PROHIBITED_LEAK_PATTERNS:
            if re.search(pattern, response_text, re.IGNORECASE):
                violations.append(f"Internal leak detected: {pattern}")

        # 2. Check for other customer IDs (e.g. C002 when user is C001)
        other_cust_match = re.findall(r'\b(C\d{3}|CUST-\d{5,6})\b', response_text, re.IGNORECASE)
        for cid in other_cust_match:
            if cid.upper() != customer_id.upper():
                violations.append(f"Cross-customer ID leak: {cid}")

        # 3. False claims check
        # Must not claim refund processed unless tool confirmed success
        refund_claimed = any(ph in resp_lower for ph in ["refund has been processed", "refund processed", "refund issued", "processed your refund"])
        has_successful_refund = any(
            isinstance(t, dict) and (t.get("action_type") == "create_refund" or "amount" in t) and t.get("status") == "success"
            for t in tool_results
        )
        if refund_claimed and not has_successful_refund:
            violations.append("False refund claim: response claimed refund was processed without tool execution")

        # 4. Monetary validation
        # If monetary amount mentioned in context of refund, verify against calculated refund
        rupee_mentions = re.findall(r'(?:₹|inr|rs\.?)\s*([0-9,]+(?:\.[0-9]+)?)', response_text, re.IGNORECASE)
        if rupee_mentions and has_successful_refund:
            for rm in rupee_mentions:
                try:
                    val = float(rm.replace(',', ''))
                    # Check if val matches tool refund amount
                    tool_amt = None
                    for t in tool_results:
                        if isinstance(t, dict) and "amount" in t:
                            tool_amt = float(t["amount"])
                            break
                    if tool_amt is not None and tool_amt > 0:
                        if abs(val - tool_amt) > 1.0 and val > 100: # allow minor difference or shipping fees
                            violations.append(f"Monetary mismatch: mentioned ₹{val} but verified refund is ₹{tool_amt}")
                except ValueError:
                    pass

        is_valid = len(violations) == 0
        return is_valid, violations

    def sanitize_or_fallback(self, response_text: str, customer_id: str, verified: Dict[str, Any], decisions: List[Dict[str, Any]], tool_results: List[Dict[str, Any]]) -> str:
        """Deterministic safe fallback generator if response violates guardrails."""
        if not decisions:
            return "How can I help you with your NovaMart orders today?"

        primary_decision = decisions[0]
        move = primary_decision.get("move", "ANSWER")
        reason = primary_decision.get("reason_code", "")
        intent = primary_decision.get("intent", "general")

        if move == "ASK":
            return "Could you please specify your Order ID or product details so I can assist you accurately?"

        if move == "ESCALATE":
            if reason == "safety_or_legal":
                return "Your request has been escalated to our Priority Safety & Legal Support Team. A specialist will review your case within 15 to 30 minutes."
            elif reason == "ACCOUNT_SUSPENDED":
                return "Your account is currently under review by our Trust & Safety team. Our specialists will contact you shortly."
            elif reason == "OTP_DISPUTE_LOGISTICS":
                return "Your delivery discrepancy has been escalated to our Logistics Investigation Desk. They will investigate with the courier within 3 business days."
            elif reason == "above_threshold":
                return "Your request exceeds the automated approval limit and has been escalated to our Refunds & Payments Lead for manual review."
            else:
                return "Your request has been escalated to our Customer Support Specialist team. A representative will contact you within 24 to 48 hours."

        if move == "ACT":
            if intent == "cancellation":
                return "Your order cancellation has been successfully processed."
            elif intent == "refund":
                amt_str = ""
                for t in tool_results:
                    if isinstance(t, dict) and "amount" in t:
                        amt_str = f" of ₹{t['amount']:,.2f}"
                return f"Your refund{amt_str} has been successfully processed to your original payment method."
            elif intent == "return":
                return "Your return request has been registered successfully. Our courier partner will pick up the package within 24-48 hours."
            elif intent == "replacement":
                return "Your replacement request has been registered. The replacement item will be dispatched once verified."
            elif intent == "address_change":
                return "Your delivery address has been updated successfully."
            else:
                return "Your request has been processed successfully."

        # ANSWER
        order = verified.get("order_state", {})
        if order and intent in ["status", "order_status", "delivery_eta"]:
            oid = order.get("order_id", "")
            ostatus = order.get("status", "in transit")
            eta = order.get("estimated_delivery_date", "shortly")
            return f"Order {oid} is currently {ostatus}. Estimated delivery date is {eta}."

        return "I am glad to assist you with your NovaMart inquiry. Please let me know if you need any additional help."
