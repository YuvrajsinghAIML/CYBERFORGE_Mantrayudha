class Verifier:
    def __init__(self, tools):
        self.tools = tools
        
    def verify_request(self, customer_id, understanding):
        results = {
            "is_valid_customer": False,
            "order_exists": False,
            "is_ambiguous": False,
            "risk_signals": [],
            "contradictions": [],
            "customer_status": "active",
            "order_state": {}
        }
        try:
            cust = self.tools.get_customer(customer_id)
            results["is_valid_customer"] = True
            results["customer_status"] = cust.get("status", "active")
        except ValueError:
            return results
            
        if results["customer_status"] == "suspended":
            results["risk_signals"].append("ACCOUNT_SUSPENDED")
            
        order_id = understanding.order_id
        if order_id:
            try:
                order = self.tools.get_order(customer_id, order_id)
                results["order_exists"] = True
                results["order_state"] = order
                
                # Check Delivery Contradictions
                # Delivered + OTP verified + customer says "not received" -> ESCALATE to Logistics
                if order.get("delivery_status") == "delivered" and "not_received" in understanding.flags:
                    results["risk_signals"].append("OTP_DISPUTE_LOGISTICS")
                    
                # Other contradictions
                if "fraud" in understanding.flags:
                    results["contradictions"].append("SUSPICIOUS_FLAGS")
                    results["risk_signals"].append("CONTRADICTION")
                    
            except ValueError:
                results["is_ambiguous"] = True
        elif understanding.intent_type != "general":
            results["is_ambiguous"] = True
            
        return results
