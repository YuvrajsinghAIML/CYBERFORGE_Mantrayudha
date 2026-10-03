import os
import pandas as pd
import json

os.makedirs('public_demo/policies', exist_ok=True)
os.makedirs('public_demo/products', exist_ok=True)
os.makedirs('public/policies', exist_ok=True)
os.makedirs('public/products', exist_ok=True)

for prefix in ['public', 'public_demo']:
    pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'status': ['active', 'active', 'suspended']
    }).to_csv(f'{prefix}/customers.csv', index=False)

    pd.DataFrame({
        'product_id': ['P001', 'P002'],
        'name': ['Laptop', 'Mouse'],
        'price': [1000.0, 50.0],
        'returnable': [True, True]
    }).to_csv(f'{prefix}/products.csv', index=False)

    pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003'],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': ['2026-05-30', '2026-06-02', '2026-06-05'],
        'status': ['delivered', 'processing', 'delivered'],
        'delivery_status': ['delivered', 'in_transit', 'delivered'],
        'estimated_delivery': ['2026-06-02', '2026-06-07', '2026-06-08'],
        'actual_delivery': ['2026-06-01', '', '2026-06-08'],
        'tracking_number': ['TRK123', 'TRK456', 'TRK789'],
        'courier': ['FastPost', 'Speedy', 'FastPost'],
        'total_amount': [1000.0, 100.0, 200000.0]
    }).to_csv(f'{prefix}/orders.csv', index=False)

    pd.DataFrame({
        'order_id': ['O001', 'O002', 'O002', 'O003'],
        'product_id': ['P001', 'P002', 'P002', 'P001'],
        'quantity': [1, 1, 1, 2],
        'price': [1000.0, 50.0, 50.0, 1000.0]
    }).to_csv(f'{prefix}/order_items.csv', index=False)

    pd.DataFrame({
        'ticket_id': ['T001'],
        'customer_id': ['C001'],
        'order_id': ['O001'],
        'status': ['open'],
        'created_at': ['2026-06-02T10:00:00Z']
    }).to_csv(f'{prefix}/support_tickets.csv', index=False)

    pd.DataFrame({
        'review_id': ['R001'],
        'product_id': ['P001'],
        'customer_id': ['C001'],
        'rating': [5]
    }).to_csv(f'{prefix}/reviews.csv', index=False)

    with open(f'{prefix}/conversations.json', 'w') as f:
        json.dump([
            {'conversation_id': 'CV001', 'customer_id': 'C001', 'order_id': 'O001', 'ticket_id': 'T001', 'messages': []},
            {'conversation_id': 'CV002', 'customer_id': 'C001', 'order_id': None, 'ticket_id': None, 'messages': []}
        ], f)

    with open(f'{prefix}/policies/return_policy.md', 'w') as f:
        f.write('# Return Policy')
    with open(f'{prefix}/products/P001.md', 'w') as f:
        f.write('# Laptop Specs')

print("Mock data and demo data updated for Phase 3.")
