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
