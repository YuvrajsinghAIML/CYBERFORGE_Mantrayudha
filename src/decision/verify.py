from typing import Dict, Any, List, Optional

class Verifier:
    def __init__(self, tools):
        self.tools = tools
        
    def verify_request(self, customer_id: str, understanding: Any) -> Dict[str, Any]:
        results = {
            "is_valid_customer": False,
            "order_exists": False,
            "is_ambiguous": False,
            "risk_signals": [],
            "contradictions": [],
            "customer_status": "active",
            "loyalty_tier": "standard",
            "order_state": {},
            "product_state": {},
            "ticket_state": {},
            "claim_count_90d": 0,
            "applicable_policy": {}
        }
        
        # 1. Verify Customer
        try:
            cust = self.tools.get_customer(customer_id)
            results["is_valid_customer"] = True
            results["customer_status"] = cust.get("status", "active")
            results["loyalty_tier"] = cust.get("loyalty_tier", "standard")
        except ValueError:
            return results
            
        if results["customer_status"] == "suspended":
            results["risk_signals"].append("ACCOUNT_SUSPENDED")
            
        # 2. Check Repeated Claims in last 90 days
        try:
            tickets = self.tools.get_support_tickets(customer_id)
            claim_tickets = [t for t in tickets if any(k in str(t.get("issue_category", "")).lower() for k in ["refund", "return", "non_delivery", "delivery", "defect"])]
            results["claim_count_90d"] = len(claim_tickets)
            if len(claim_tickets) >= 3:
                results["risk_signals"].append("REPEATED_CLAIMS")
        except Exception:
            pass

        # 3. Security & Safety Flags
        if "injection_attempt" in understanding.flags:
            results["risk_signals"].append("INJECTION_ATTEMPT")
            
        if "ownership_violation" in understanding.flags:
            results["risk_signals"].append("ORDER_NOT_OWNED")
            results["is_ambiguous"] = True

        # 4. Check Alternate Refund Destination
        # e.g., "refund to another card", "send to friend's upi"
        msg_text = getattr(understanding, "untrusted_input_sanitized", "") or ""
        msg_lower = msg_text.lower()
        if any(ph in msg_lower for ph in ["different account", "different card", "another card", "another upi", "friend's account", "my brother's account", "different bank"]):
            results["risk_signals"].append("DIFFERENT_REFUND_DESTINATION")

        # 5. Verify Order & Items
        order_id = understanding.order_id
        if order_id:
            try:
                order = self.tools.get_order(customer_id, order_id)
                results["order_exists"] = True
                results["order_state"] = order
                
                # Check delivery status
                del_status = str(order.get("delivery_status", order.get("status", ""))).lower()
                otp_verified = bool(order.get("delivery_otp_verified", False))
                
                # OTP dispute: delivered + customer claims not received
                if del_status == "delivered" and "not_received" in understanding.flags:
                    results["risk_signals"].append("OTP_DISPUTE_LOGISTICS")
                    
                # High value threshold check
                total_amt = float(order.get("total_amount", 0))
                # v1 threshold is 100k, v2 threshold is 75k
                order_date = str(order.get("order_date", "2026-06-01"))
                policy = self.tools.policy_engine.get_applicable_policy(order_date)
                results["applicable_policy"] = policy
                threshold = 75000.0 if policy.get("version") == "v2" else 100000.0
                if total_amt > threshold:
                    results["risk_signals"].append("HIGH_VALUE_THRESHOLD")

                if "fraud" in understanding.flags:
                    results["contradictions"].append("SUSPICIOUS_FLAGS")
                    results["risk_signals"].append("CONTRADICTION")
                    
            except ValueError:
                # Order does not exist or does not belong to customer
                results["order_exists"] = False
                results["is_ambiguous"] = True
        elif getattr(understanding, "intent_type", "general") != "general" or getattr(understanding, "requires_clarification", False):
            results["is_ambiguous"] = True
            
        return results
