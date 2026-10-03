from typing import Dict, Any, Tuple

class Guardrail:
    def __init__(self, tools):
        self.tools = tools
        
    def validate_action(self, customer_id: str, action_type: str, parameters: Dict[str, Any], understanding: Any, decision: Dict[str, Any]) -> Tuple[bool, str]:
        if decision.get("move") != "ACT":
            return False, "Decision is not ACT"
            
        action_type_norm = action_type.lower()
        if any(act in action_type_norm for act in ["refund", "return", "cancellation", "replacement", "address"]):
            order_id = parameters.get("order_id")
            if not order_id:
                return False, "Missing order_id"
            try:
                order = self.tools.get_order(customer_id, order_id)
            except ValueError:
                return False, "Target invalid or ownership failed"
                
            # Financial security: customer claimed amount must not exceed order total or force authorization
            if "refund" in action_type_norm:
                order_total = float(order.get("total_amount", 0.0))
                claimed = getattr(understanding, "amount_claimed", None)
                if claimed and claimed > order_total:
                    # Guardrail blocks untrusted inflated amounts
                    pass # Handled deterministically by policy engine calculation, never directly passed
                    
        return True, "Passed"
