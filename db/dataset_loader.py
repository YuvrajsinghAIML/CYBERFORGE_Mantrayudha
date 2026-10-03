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
        
        with open(base_path / "conversations.json", 'r', encoding='utf-8') as f:
            datasets["conversations"] = json.load(f)
            
    except FileNotFoundError as e:
        raise DataValidationError(f"Missing required dataset file: {e}")
        
    # --- NORMALIZATION LAYER ---
    
    # Order date is YYYY-MM-DD HH:MM:SS in official, policy engine expects YYYY-MM-DD
    if "order_date" in datasets["orders"].columns:
        datasets["orders"]["order_date"] = datasets["orders"]["order_date"].astype(str).str.split(" ").str[0]
        
    # Customers needs 'status' for internal logic, official has 'account_status'
    if "account_status" in datasets["customers"].columns and "status" not in datasets["customers"].columns:
        datasets["customers"].rename(columns={"account_status": "status"}, inplace=True)
        
    # Orders needs 'status', official has 'order_status'
    if "order_status" in datasets["orders"].columns and "status" not in datasets["orders"].columns:
        datasets["orders"].rename(columns={"order_status": "status"}, inplace=True)

    # Validation constraints
    required_customer_cols = {"customer_id", "first_name", "email", "status"}
    if not required_customer_cols.issubset(datasets["customers"].columns):
        raise DataValidationError("Customers dataset is missing required columns")
        
    # Integrity check: customer -> orders
    if not datasets["orders"]["customer_id"].isin(datasets["customers"]["customer_id"]).all():
        raise DataValidationError("Order references non-existent customer")
        
    # Integrity check: order -> order_items
    if not datasets["order_items"]["order_id"].isin(datasets["orders"]["order_id"]).all():
        raise DataValidationError("Order item references non-existent order")
        
    # Integrity check: order_item -> product
    if not datasets["order_items"]["product_id"].isin(datasets["products"]["product_id"]).all():
        raise DataValidationError("Order item references non-existent product")
        
    # Relationship validation for optional/required links
    # Tickets customer_id is required
    if not datasets["support_tickets"]["customer_id"].isin(datasets["customers"]["customer_id"]).all():
        raise DataValidationError("Support ticket references non-existent customer")
        
    return datasets
