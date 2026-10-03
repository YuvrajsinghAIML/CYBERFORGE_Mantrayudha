from typing import Dict, Any

class Tools:
    def __init__(self, datasets, action_log, policy_engine):
        self.datasets = datasets
        self.action_log = action_log
        self.policy_engine = policy_engine

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        df = self.datasets["customers"]
        cust = df[df["customer_id"] == customer_id]
        if cust.empty:
            raise ValueError("Customer not found")
        return cust.iloc[0].to_dict()

    def get_order(self, customer_id: str, order_id: str) -> Dict[str, Any]:
        df = self.datasets["orders"]
        order = df[(df["order_id"] == order_id) & (df["customer_id"] == customer_id)]
        if order.empty:
            raise ValueError("Order not found or does not belong to customer")
        
        items_df = self.datasets["order_items"]
        items = items_df[items_df["order_id"] == order_id].to_dict('records')
        
        result = order.iloc[0].to_dict()
        result["items"] = items
        return result

    def get_product(self, product_id: str) -> Dict[str, Any]:
        df = self.datasets["products"]
        prod = df[df["product_id"] == product_id]
        if prod.empty:
            raise ValueError("Product not found")
        return prod.iloc[0].to_dict()

    def get_conversations(self, customer_id: str, order_id: str = None, ticket_id: str = None) -> Dict[str, Any]:
        # Fix: Search conversations by customer_id directly rather than assuming ticket match
        convos = self.datasets.get("conversations", [])
        matched = []
        for c in convos:
            if c.get("customer_id") == customer_id:
                if order_id and c.get("order_id") != order_id:
                    continue
                if ticket_id and c.get("ticket_id") != ticket_id:
                    continue
                matched.append(c)
        return {"conversations": matched}

    def check_refund_eligibility(self, customer_id: str, order_id: str, current_date: str) -> Dict[str, Any]:
        order = self.get_order(customer_id, order_id)
        eligible, policy = self.policy_engine.is_eligible_for_return(order["order_date"], current_date)
        return {
            "eligible": eligible,
            "policy_version": policy["version"],
            "order_date": order["order_date"],
            "current_date": current_date
        }

    def calculate_refund(self, customer_id: str, order_id: str, item_id: str, category: str, item_price: float) -> Dict[str, Any]:
        order = self.get_order(customer_id, order_id)
        policy = self.policy_engine.get_applicable_policy(order["order_date"])
        refund_amount = self.policy_engine.calculate_refund(item_price, category, policy)
        return {
            "refund_amount": refund_amount,
            "policy_version": policy["version"]
        }

    def create_return(self, customer_id: str, order_id: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_return", customer_id, {"order_id": order_id})
        return {"status": "success", "action_id": action_id}

    def create_refund(self, customer_id: str, order_id: str, amount: float) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_refund", customer_id, {"order_id": order_id}, {"amount": amount})
        return {"status": "success", "action_id": action_id}

    def create_support_ticket(self, customer_id: str, order_id: str, issue: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_ticket", customer_id, {"order_id": order_id}, {"issue": issue})
        return {"status": "success", "action_id": action_id}

    def escalate_to_human(self, customer_id: str, order_id: str, team: str, priority: str, reason: str) -> Dict[str, Any]:
        if order_id:
            self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("escalate", customer_id, {"order_id": order_id}, {"team": team, "priority": priority, "reason": reason})
        return {"status": "success", "action_id": action_id}
