import os
from db.dataset_loader import load_datasets

# Don't force demo mode anymore! Let it use whatever is set, defaulting to official
datasets = load_datasets()

# Find dynamic IDs based on conditions
active_customers = datasets["customers"][datasets["customers"]["status"] == "active"]
suspended_customers = datasets["customers"][datasets["customers"]["status"] == "suspended"]

GLOBAL_C001 = active_customers["customer_id"].iloc[0]
GLOBAL_C002 = active_customers["customer_id"].iloc[1]
GLOBAL_C003 = suspended_customers["customer_id"].iloc[0]

GLOBAL_O001 = datasets["orders"][datasets["orders"]["customer_id"] == GLOBAL_C001]["order_id"].iloc[0]
GLOBAL_O002 = datasets["orders"][datasets["orders"]["customer_id"] == GLOBAL_C002]["order_id"].iloc[0]
c3_orders = datasets["orders"][datasets["orders"]["customer_id"] == GLOBAL_C003]["order_id"]
GLOBAL_O003 = c3_orders.iloc[0] if not c3_orders.empty else GLOBAL_O001

GLOBAL_P001 = datasets["products"]["product_id"].iloc[0]
GLOBAL_T001 = datasets["support_tickets"]["ticket_id"].iloc[0]
GLOBAL_CONV001 = datasets["conversations"][0]["conversation_id"] if len(datasets["conversations"]) > 0 else "CONV-001"
