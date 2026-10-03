import os
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any

class DataValidationError(Exception):
    pass

def load_datasets() -> Dict[str, Any]:
    mode = os.getenv("NOVAMART_DATA_MODE", "official")
    
    if mode == "demo":
        base_path = Path("demo_data")
    else:
        base_path = Path("public")
        
    if not base_path.exists() or not any(base_path.iterdir()):
        raise DataValidationError(f"Official dataset is missing in {base_path}/")
        
    datasets = {}
    
    try:
        datasets["customers"] = pd.read_csv(base_path / "customers.csv")
        datasets["orders"] = pd.read_csv(base_path / "orders.csv")
        datasets["order_items"] = pd.read_csv(base_path / "order_items.csv")
        datasets["products"] = pd.read_csv(base_path / "products.csv")
        datasets["support_tickets"] = pd.read_csv(base_path / "support_tickets.csv")
        datasets["reviews"] = pd.read_csv(base_path / "reviews.csv")
        
        with open(base_path / "conversations.json", 'r') as f:
            datasets["conversations"] = json.load(f)
            
    except FileNotFoundError as e:
        raise DataValidationError(f"Missing required dataset file: {e}")
        
    # Schema validation (example constraints)
    required_customer_cols = {"customer_id", "name", "email", "status"}
    if not required_customer_cols.issubset(datasets["customers"].columns):
        raise DataValidationError("Customers dataset is missing required columns")
        
    # Integrity check
    if not datasets["orders"]["customer_id"].isin(datasets["customers"]["customer_id"]).all():
        raise DataValidationError("Order references non-existent customer")
        
    return datasets
