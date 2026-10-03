import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. db/dataset_loader.py
write_file('db/dataset_loader.py', """
import pandas as pd
import json
from pathlib import Path
import os

class DataValidationError(Exception):
    pass

def load_datasets(use_demo=False):
    base_dir = Path(__file__).resolve().parent.parent
    real_pub = base_dir / "public"
    demo_pub = base_dir / "public_demo"
    
    pub = real_pub
    if use_demo:
        pub = demo_pub
    
    if not pub.exists() or not pub.is_dir():
        if use_demo:
            raise DataValidationError(f"Demo data directory not found: {pub}")
        else:
            raise DataValidationError(f"Real data directory not found: {pub}")
            
    files = {
        "customers": pub / "customers.csv",
        "products": pub / "products.csv",
        "orders": pub / "orders.csv",
        "order_items": pub / "order_items.csv",
        "support_tickets": pub / "support_tickets.csv",
        "reviews": pub / "reviews.csv",
        "conversations": pub / "conversations.json"
    }
    
    for name, path in files.items():
        if not path.exists():
            raise DataValidationError(f"Required dataset missing: {name} at {path}")
            
    customers = pd.read_csv(files["customers"])
    products = pd.read_csv(files["products"])
    orders = pd.read_csv(files["orders"])
    order_items = pd.read_csv(files["order_items"])
    support_tickets = pd.read_csv(files["support_tickets"])
    reviews = pd.read_csv(files["reviews"])
    
    with open(files["conversations"], "r") as f:
        conversations = json.load(f)
        
    # Validation: Uniqueness
    if not customers['customer_id'].is_unique:
        raise DataValidationError("customers dataset has duplicate customer_id")
    if not products['product_id'].is_unique:
        raise DataValidationError("products dataset has duplicate product_id")
    if not orders['order_id'].is_unique:
        raise DataValidationError("orders dataset has duplicate order_id")
    if not support_tickets['ticket_id'].is_unique:
        raise DataValidationError("support_tickets dataset has duplicate ticket_id")
        
    # Validation: Foreign Keys
    missing_customers = set(orders['customer_id']) - set(customers['customer_id'])
    if missing_customers:
        raise DataValidationError(f"orders dataset has missing customer_id relationships: {missing_customers}")
        
    missing_orders = set(order_items['order_id']) - set(orders['order_id'])
    if missing_orders:
        raise DataValidationError(f"order_items dataset has missing order_id relationships: {missing_orders}")
        
    missing_products = set(order_items['product_id']) - set(products['product_id'])
    if missing_products:
        raise DataValidationError(f"order_items dataset has missing product_id relationships: {missing_products}")
        
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "support_tickets": support_tickets,
        "reviews": reviews,
        "conversations": conversations
    }
""")

# 2. config/config_loader.py
write_file('config/config_loader.py', """
import yaml
import glob
from pathlib import Path

class PolicyConfigError(Exception):
    pass

def load_policies_config(filepath="config/policies.yaml"):
    base_dir = Path(__file__).resolve().parent.parent
    policy_path = base_dir / filepath
    if not policy_path.exists():
        raise PolicyConfigError(f"Policy config not found: {policy_path}")
    with open(policy_path, 'r') as f:
        return yaml.safe_load(f)

def discover_policy_documents(public_dir="public"):
    base_dir = Path(__file__).resolve().parent.parent
    policies_dir = base_dir / public_dir / "policies"
    if not policies_dir.exists():
        raise PolicyConfigError(f"Policies directory not found: {policies_dir}")
        
    documents = {}
    for filepath in policies_dir.glob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            documents[filepath.stem] = f.read()
            
    if not documents:
        raise PolicyConfigError(f"No policy documents found in {policies_dir}")
        
    return documents
""")

# 3. src/contracts.py
write_file('src/contracts.py', """
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any

class UnderstandingContract(BaseModel):
    intents: List[str]
    intent_type: str = "general"
    order_id: Optional[str] = None
    reason: Optional[str] = None
    topic: Optional[str] = None
    amount_claimed: Optional[float] = None
    flags: List[str] = Field(default_factory=list)
    evidence_provided: bool = False
    language: str = "en"
    
    @model_validator(mode='after')
    def check_intents(self) -> 'UnderstandingContract':
        if not self.intents:
            raise ValueError("Intents list cannot be empty")
        valid_intents = {"refund", "return", "cancellation", "status", "escalate", "general", "replacement"}
        for intent in self.intents:
            if intent not in valid_intents:
                raise ValueError(f"Invalid intent: {intent}")
        return self

class TraceContract(BaseModel):
    understanding: UnderstandingContract
    verification: Dict[str, Any] = Field(default_factory=dict)
    policy: Dict[str, Any] = Field(default_factory=dict)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    guard: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
""")

# 4. src/action_log.py
write_file('src/action_log.py', """
from datetime import datetime
import uuid
import zoneinfo

class ActionLog:
    def __init__(self):
        self.logs = []
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        
    def record_action(self, action_type, customer_id, identifiers, parameters=None):
        # Idempotency check
        for log in self.logs:
            if log["action_type"] == action_type and log["customer_id"] == customer_id and log["identifiers"] == identifiers:
                return log["action_id"] # Return existing action ID if identical action already performed
                
        action_id = str(uuid.uuid4())
        self.logs.append({
            "action_id": action_id,
            "action_type": action_type,
            "customer_id": customer_id,
            "identifiers": identifiers,
            "parameters": parameters or {},
            "timestamp": datetime.now(self.tz).isoformat()
        })
        return action_id
        
    def get_logs(self):
        return self.logs
""")

# 5. src/policy_engine.py
write_file('src/policy_engine.py', """
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
""")

# 6. src/tools.py
write_file('src/tools.py', """
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

    def get_conversations(self, customer_id: str) -> Dict[str, Any]:
        # For simplicity, returning all from json where ticket belongs to customer
        df = self.datasets["support_tickets"]
        tickets = df[df["customer_id"] == customer_id]["ticket_id"].tolist()
        
        convos = [c for c in self.datasets["conversations"] if c.get("ticket_id") in tickets]
        return {"conversations": convos}

    def check_refund_eligibility(self, customer_id: str, order_id: str, current_date: str) -> Dict[str, Any]:
        order = self.get_order(customer_id, order_id)
        # simplistic eligibility check
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
        # Validate order exists
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_return", customer_id, {"order_id": order_id})
        return {"status": "success", "action_id": action_id}

    def create_refund(self, customer_id: str, order_id: str, amount: float) -> Dict[str, Any]:
        # Validate order exists
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_refund", customer_id, {"order_id": order_id}, {"amount": amount})
        return {"status": "success", "action_id": action_id}

    def create_support_ticket(self, customer_id: str, order_id: str, issue: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("create_ticket", customer_id, {"order_id": order_id}, {"issue": issue})
        return {"status": "success", "action_id": action_id}

    def escalate_to_human(self, customer_id: str, order_id: str, team: str, priority: str, reason: str) -> Dict[str, Any]:
        self.get_order(customer_id, order_id)
        action_id = self.action_log.record_action("escalate", customer_id, {"order_id": order_id}, {"team": team, "priority": priority, "reason": reason})
        return {"status": "success", "action_id": action_id}
""")

print("Harden script generated.")
