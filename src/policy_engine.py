from datetime import datetime, timedelta
import zoneinfo

class PolicyEngine:
    def __init__(self, config_versions):
        self.versions = sorted(config_versions, key=lambda x: x["effective_from"])
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")

    def get_applicable_policy(self, order_date_str):
        order_date = datetime.strptime(order_date_str, "%Y-%m-%d").date()
        applicable = None
        for v in self.versions:
            effective_date = datetime.strptime(v["effective_from"], "%Y-%m-%d").date()
            if effective_date <= order_date:
                applicable = v
        if not applicable:
            raise ValueError("No applicable policy found for order date")
        return applicable
        
    def calculate_refund_window(self, policy, loyalty_tier="standard"):
        window = policy["return_window_days"]
        if loyalty_tier == "gold":
            window += 2
        elif loyalty_tier == "platinum":
            window += 3
        return window

    def is_eligible_for_return(self, order_date_str, current_date_str, loyalty_tier="standard"):
        policy = self.get_applicable_policy(order_date_str)
        window = self.calculate_refund_window(policy, loyalty_tier)
        
        order_date = datetime.strptime(order_date_str, "%Y-%m-%d").date()
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        
        days_passed = (current_date - order_date).days
        return days_passed <= window, policy

    def calculate_refund(self, item_price, category, policy):
        restocking_fee = 0
        if policy["version"] == "v2" and category in ["Laptop", "Tablet", "Camera", "Monitor"]:
            restocking_fee = item_price * (policy["restocking_fee_percent"] / 100.0)
            if restocking_fee > 2500:
                restocking_fee = 2500
        
        final_refund = item_price - restocking_fee
        return max(0, final_refund)
