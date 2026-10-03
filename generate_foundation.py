import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')

# config/policies.yaml
write_file('config/policies.yaml', """
versions:
  - version: "v1"
    effective_from: "2020-01-01"
    return_window_days: 15
    restocking_fee_percent: 0
  - version: "v2"
    effective_from: "2026-06-01"
    return_window_days: 30
    restocking_fee_percent: 10
""")

write_file('config/policies_demo_v3.yaml', """
versions:
  - version: "v3"
    effective_from: "2027-01-01"
    return_window_days: 45
    restocking_fee_percent: 5
""")

# config/config_loader.py
write_file('config/config_loader.py', """
import yaml
from pathlib import Path

def load_policies(filepath="config/policies.yaml"):
    base_dir = Path(__file__).resolve().parent.parent
    policy_path = base_dir / filepath
    with open(policy_path, 'r') as f:
        return yaml.safe_load(f)
""")

# db/dataset_loader.py
write_file('db/dataset_loader.py', """
import pandas as pd
import json
from pathlib import Path

def load_datasets(public_dir="public"):
    base_dir = Path(__file__).resolve().parent.parent
    pub = base_dir / public_dir
    
    customers = pd.read_csv(pub / "customers.csv")
    products = pd.read_csv(pub / "products.csv")
    orders = pd.read_csv(pub / "orders.csv")
    order_items = pd.read_csv(pub / "order_items.csv")
    support_tickets = pd.read_csv(pub / "support_tickets.csv")
    reviews = pd.read_csv(pub / "reviews.csv")
    
    with open(pub / "conversations.json", "r") as f:
        conversations = json.load(f)
        
    # Validate relationships
    assert set(orders['customer_id']).issubset(set(customers['customer_id'])), "Invalid customer_id in orders"
    assert set(order_items['order_id']).issubset(set(orders['order_id'])), "Invalid order_id in order_items"
    assert set(order_items['product_id']).issubset(set(products['product_id'])), "Invalid product_id in order_items"
    
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

# src/action_log.py
write_file('src/action_log.py', """
from datetime import datetime
import uuid
import zoneinfo

class ActionLog:
    def __init__(self):
        self.logs = []
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        
    def record_action(self, action_type, identifiers, context=None):
        action_id = str(uuid.uuid4())
        self.logs.append({
            "action_id": action_id,
            "action_type": action_type,
            "identifiers": identifiers,
            "context": context,
            "timestamp": datetime.now(self.tz).isoformat()
        })
        return action_id
        
    def get_logs(self):
        return self.logs
""")

# src/contracts.py
write_file('src/contracts.py', """
from pydantic import BaseModel, Field
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

class TraceContract(BaseModel):
    understanding: UnderstandingContract
    verification: Dict[str, Any] = Field(default_factory=dict)
    policy: Dict[str, Any] = Field(default_factory=dict)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    guard: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
""")

# src/metrics.py
write_file('src/metrics.py', """
class MetricsManager:
    def __init__(self):
        self.metrics = {}
        
    def record(self, key, value):
        self.metrics[key] = value
""")

# tests/test_foundation.py
write_file('tests/test_foundation.py', """
import pytest
from db.dataset_loader import load_datasets
from config.config_loader import load_policies
from src.action_log import ActionLog
from src.contracts import UnderstandingContract, TraceContract
from pydantic import ValidationError

def test_load_datasets():
    datasets = load_datasets()
    assert "customers" in datasets
    assert len(datasets["customers"]) > 0

def test_load_policies():
    policies = load_policies()
    assert "versions" in policies
    assert len(policies["versions"]) > 0
    
def test_action_log():
    log = ActionLog()
    action_id = log.record_action("refund", {"order_id": "O001"})
    assert len(log.get_logs()) == 1
    assert log.get_logs()[0]["action_id"] == action_id
    assert "Asia/Kolkata" in log.get_logs()[0]["timestamp"] or "+" in log.get_logs()[0]["timestamp"]

def test_understanding_contract_valid():
    contract = UnderstandingContract(intents=["refund"], order_id="O001")
    assert contract.intents == ["refund"]

def test_understanding_contract_invalid():
    with pytest.raises(ValidationError):
        UnderstandingContract(intents="not-a-list")
""")

# README.md
write_file('README.md', """
# NovaMart AI Customer Support Agent

## Purpose
NovaMart AI Agent backend foundation.

## Environment
- Python 3.11

## Installation
```
pip install -r requirements.txt
```

## Running Tests
```
pytest -q
```
""")

# requirements.txt
write_file('requirements.txt', """
pandas
pyyaml
pydantic
pytest
""")

print("Foundation files generated")
