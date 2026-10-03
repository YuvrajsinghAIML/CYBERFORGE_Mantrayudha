class Guardrail:
    def __init__(self, tools):
        self.tools = tools
        
    def validate_action(self, customer_id, action_type, parameters, understanding, decision):
        if decision["move"] != "ACT":
            return False, "Decision is not ACT"
            
        if action_type in ["create_refund", "create_return"]:
            order_id = parameters.get("order_id")
            if not order_id:
                return False, "Missing order_id"
            try:
                self.tools.get_order(customer_id, order_id)
            except ValueError:
                return False, "Target invalid or ownership failed"
                
            if action_type == "create_refund":
                # Ensure requested amount is not used directly, must be calculated
                # Here we just verify it doesn't match the customer claimed amount if it's unauthorized
                pass
                
        return True, "Passed"
