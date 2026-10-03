import os
from pathlib import Path
from typing import Dict, Any, List, Optional

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
        
        result = prod.iloc[0].to_dict()
        category = result.get("category", "").lower()
        
        mode = os.getenv("NOVAMART_DATA_MODE", "official")
        base_path = Path("demo_data/products") if mode == "demo" else Path("public/products")
        spec_path = base_path / f"{category}.md"
        
        if spec_path.exists():
            with open(spec_path, 'r', encoding='utf-8') as f:
                result["specification"] = f.read()
                
        return result

    def get_conversations(self, customer_id: str, order_id: Optional[str] = None, ticket_id: Optional[str] = None) -> Dict[str, Any]:
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

    def get_support_tickets(self, customer_id: str, ticket_id: Optional[str] = None) -> List[Dict[str, Any]]:
        df = self.datasets.get("support_tickets")
        if df is None or df.empty:
            return []
        if ticket_id:
            matched = df[(df["customer_id"] == customer_id) & (df["ticket_id"] == ticket_id)]
        else:
            matched = df[df["customer_id"] == customer_id]
        return matched.to_dict('records')

    def check_refund_eligibility(self, customer_id: str, order_id: str, current_date: str) -> Dict[str, Any]:
        order = self.get_order(customer_id, order_id)
        cust = self.get_customer(customer_id)
        tier = cust.get("loyalty_tier", "standard")
        eligible, policy = self.policy_engine.is_eligible_for_return(order["order_date"], current_date, loyalty_tier=tier)
        return {
            "eligible": eligible,
            "policy_version": policy["version"],
            "order_date": order["order_date"],
            "current_date": current_date,
            "loyalty_tier": tier
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
        return {"status": "success", "action_id": action_id, "action_type": "create_return", "order_id": order_id}

    def create_refund(self, customer_id: str, order_id: str, amount: float) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_refund", customer_id, {"order_id": order_id}, {"amount": amount})
        return {"status": "success", "action_id": action_id, "action_type": "create_refund", "order_id": order_id, "amount": amount}

    def create_cancellation(self, customer_id: str, order_id: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_cancellation", customer_id, {"order_id": order_id})
        return {"status": "success", "action_id": action_id, "action_type": "create_cancellation", "order_id": order_id}

    def create_replacement(self, customer_id: str, order_id: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_replacement", customer_id, {"order_id": order_id})
        return {"status": "success", "action_id": action_id, "action_type": "create_replacement", "order_id": order_id}

    def update_address(self, customer_id: str, order_id: str, new_address: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("update_address", customer_id, {"order_id": order_id}, {"new_address": new_address})
        return {"status": "success", "action_id": action_id, "action_type": "update_address", "order_id": order_id, "new_address": new_address}

    def issue_goodwill_credit(self, customer_id: str, order_id: str, amount: float) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        capped_amount = min(amount, 300.0) # Tier 1 goodwill cap per shipping policy
        action_id = self.action_log.record_action("goodwill_credit", customer_id, {"order_id": order_id}, {"amount": capped_amount})
        return {"status": "success", "action_id": action_id, "action_type": "goodwill_credit", "amount": capped_amount}

    def create_support_ticket(self, customer_id: str, order_id: Optional[str], issue: str) -> Dict[str, Any]:
        if order_id:
            try:
                self.get_order(customer_id, order_id)
            except ValueError:
                pass
        action_id = self.action_log.record_action("create_ticket", customer_id, {"order_id": order_id}, {"issue": issue})
        return {"status": "success", "action_id": action_id, "action_type": "create_ticket", "issue": issue}

    def escalate_to_human(self, customer_id: str, order_id: Optional[str], team: str, priority: str, reason: str) -> Dict[str, Any]:
        if order_id:
            try:
                self.get_order(customer_id, order_id)
            except ValueError:
                pass
        action_id = self.action_log.record_action("escalate", customer_id, {"order_id": order_id}, {"team": team, "priority": priority, "reason": reason})
        return {"status": "success", "action_id": action_id, "action_type": "escalate", "team": team, "priority": priority, "reason": reason}
