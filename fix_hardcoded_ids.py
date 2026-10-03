import os
import re

def update_test(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove conftest setting demo mode
    if 'conftest.py' in path:
        content = content.replace('os.environ["NOVAMART_DATA_MODE"] = "demo"', 'os.environ["NOVAMART_DATA_MODE"] = "official"')
    
    # Replace "C001" with a dynamically fetched customer ID
    # In tests, `datasets` is available because they call `datasets = load_datasets()`
    content = content.replace('"C001"', 'datasets["customers"]["customer_id"].iloc[0]')
    content = content.replace('"C002"', 'datasets["customers"]["customer_id"].iloc[1]')
    content = content.replace('"O001"', 'datasets["orders"]["order_id"].iloc[0]')
    content = content.replace('"O002"', 'datasets["orders"]["order_id"].iloc[1]')
    content = content.replace('"O003"', 'datasets["orders"]["order_id"].iloc[2]')
    content = content.replace('"P001"', 'datasets["products"]["product_id"].iloc[0]')
    content = content.replace('"T001"', 'datasets["support_tickets"]["ticket_id"].iloc[0]')
    content = content.replace('"CONV001"', 'datasets["conversations"][0]["conversation_id"]')
    
    # We must fix string interpolations, e.g. if it was `get_customer("C001")`, 
    # it becomes `get_customer(datasets["customers"]["customer_id"].iloc[0])`
    # Let's just do literal string replacements.
    
    # Also fix some specific tests like test_decider_otp_dispute
    # Instead of doing naive string replacements, I will just rewrite the test files
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            update_test(os.path.join(root, file))

print("Fixed hardcoded IDs in tests")
