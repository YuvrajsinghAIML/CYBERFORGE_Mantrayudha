from datetime import datetime, timedelta
import zoneinfo
import copy
from typing import List, Dict, Any, Tuple, Optional

class PolicyEngine:
    def __init__(self, config_versions: List[Dict[str, Any]]):
        self.base_versions = copy.deepcopy(config_versions)
        self.versions = sorted(config_versions, key=lambda x: x["effective_from"])
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        self.is_mutated = False

    def apply_mutation(self, mutation_versions: List[Dict[str, Any]]):
        """Used by Policy Lab to test config mutation in memory without code changes."""
        self.versions = sorted(mutation_versions, key=lambda x: x["effective_from"])
        self.is_mutated = True

    def restore_base_config(self):
        """Restores base policy versions after Policy Lab run."""
        self.versions = sorted(copy.deepcopy(self.base_versions), key=lambda x: x["effective_from"])
        self.is_mutated = False

    def get_applicable_policy(self, order_date_str: str) -> Dict[str, Any]:
        # Handle datetime strings like "2026-06-01 12:30:00"
        clean_date = str(order_date_str).split(" ")[0]
        order_date = datetime.strptime(clean_date, "%Y-%m-%d").date()
        applicable = None
        for v in self.versions:
            effective_date = datetime.strptime(v["effective_from"], "%Y-%m-%d").date()
            if effective_date <= order_date:
                applicable = v
        if not applicable:
            # Fallback to the first version if older than initial date
            if self.versions:
                return self.versions[0]
            raise ValueError("No applicable policy found for order date")
        return applicable
        
    def calculate_refund_window(self, policy: Dict[str, Any], loyalty_tier: str = "standard", is_defect: bool = False) -> int:
        tier = (loyalty_tier or "standard").lower()
        base_window = policy.get("return_window_days", 7)
        if is_defect:
            # Defect window in v2 is 10 days, in v1 is 15 days
            base_window = 10 if policy.get("version") == "v2" else 15
        
        # Loyalty extensions apply to change-of-mind returns
        if not is_defect:
            if tier == "gold":
                base_window += 2
            elif tier == "platinum":
                base_window += 3
        return base_window

    def is_eligible_for_return(self, order_date_str: str, current_date_str: str, loyalty_tier: str = "standard", is_defect: bool = False) -> Tuple[bool, Dict[str, Any]]:
        policy = self.get_applicable_policy(order_date_str)
        window = self.calculate_refund_window(policy, loyalty_tier, is_defect)
        
        order_clean = str(order_date_str).split(" ")[0]
        current_clean = str(current_date_str).split(" ")[0]
        order_date = datetime.strptime(order_clean, "%Y-%m-%d").date()
        current_date = datetime.strptime(current_clean, "%Y-%m-%d").date()
        
        days_passed = (current_date - order_date).days
        return days_passed <= window, policy

    def calculate_refund(self, item_price: float, category: str, policy: Dict[str, Any]) -> float:
        restocking_fee = 0.0
        cat_lower = (category or "").lower()
        restock_categories = ["laptop", "tablet", "camera", "monitor", "tablets", "cameras", "monitors", "laptops"]
        
        fee_percent = policy.get("restocking_fee_percent", 0)
        ver = policy.get("version", "v1")
        
        if fee_percent > 0 and any(c == cat_lower for c in restock_categories):
            max_cap = policy.get("max_restocking_fee", 2500.0 if ver == "v2" else 5000.0)
            calculated_fee = item_price * (fee_percent / 100.0)
            restocking_fee = min(calculated_fee, max_cap)
        
        final_refund = item_price - restocking_fee
        return max(0.0, float(final_refund))
