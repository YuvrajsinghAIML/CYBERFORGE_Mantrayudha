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
