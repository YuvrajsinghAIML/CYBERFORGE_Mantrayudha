import os
import pandas as pd
import json

os.makedirs('public/policies', exist_ok=True)
os.makedirs('public/products', exist_ok=True)

# Customers
pd.DataFrame({
    'customer_id': ['C001', 'C002'],
    'name': ['Alice', 'Bob'],
    'email': ['alice@example.com', 'bob@example.com']
}).to_csv('public/customers.csv', index=False)

# Products
pd.DataFrame({
    'product_id': ['P001', 'P002'],
    'name': ['Laptop', 'Mouse'],
    'price': [1000.0, 50.0]
}).to_csv('public/products.csv', index=False)

# Orders
pd.DataFrame({
    'order_id': ['O001', 'O002'],
    'customer_id': ['C001', 'C002'],
    'order_date': ['2026-05-30', '2026-06-02'],
    'status': ['delivered', 'processing']
}).to_csv('public/orders.csv', index=False)

# Order Items
pd.DataFrame({
    'order_id': ['O001', 'O002'],
    'product_id': ['P001', 'P002'],
    'quantity': [1, 2],
    'price': [1000.0, 50.0]
}).to_csv('public/order_items.csv', index=False)

# Support Tickets
pd.DataFrame({
    'ticket_id': ['T001'],
    'customer_id': ['C001'],
    'order_id': ['O001'],
    'status': ['open']
}).to_csv('public/support_tickets.csv', index=False)

# Reviews
pd.DataFrame({
    'review_id': ['R001'],
    'product_id': ['P001'],
    'customer_id': ['C001'],
    'rating': [5]
}).to_csv('public/reviews.csv', index=False)

# Conversations
with open('public/conversations.json', 'w') as f:
    json.dump([{'conversation_id': 'CV001', 'ticket_id': 'T001', 'messages': []}], f)

# Policies
with open('public/policies/return_policy.md', 'w') as f:
    f.write('# Return Policy')
    
# Product Specs
with open('public/products/P001.md', 'w') as f:
    f.write('# Laptop Specs')

print("Mock data generated")
