import pandas as pd
import json
import glob
from collections import defaultdict

def analyze_csv(path):
    df = pd.read_csv(path)
    print(f"\n--- {path} ---")
    print(f"Record Count: {len(df)}")
    print("Columns: " + ", ".join(df.columns))
    print("Missing Values:")
    print(df.isnull().sum())
    
    # ID formats and Date formats heuristically
    for col in df.columns:
        if 'id' in col.lower() or col.lower().endswith('_id'):
            sample = df[col].dropna().head(3).tolist()
            print(f"  {col} format sample: {sample}")
        if 'date' in col.lower() or 'created' in col.lower():
            sample = df[col].dropna().head(3).tolist()
            print(f"  {col} format sample: {sample}")
        if 'status' in col.lower():
            statuses = df[col].unique().tolist()
            print(f"  {col} enum values: {statuses}")

def main():
    print("ANALYZING OFFICIAL DATASET")
    for csv in glob.glob("public/*.csv"):
        analyze_csv(csv)
        
    with open("public/conversations.json", "r", encoding="utf-8") as f:
        convs = json.load(f)
        print("\n--- public/conversations.json ---")
        print(f"Record Count: {len(convs)}")
        if len(convs) > 0:
            keys = set()
            for c in convs:
                keys.update(c.keys())
            print(f"JSON Keys: {list(keys)}")
            print(f"First conversation sample identifiers: ID={convs[0].get('conversation_id')}, CUST={convs[0].get('customer_id')}, ORD={convs[0].get('order_id')}, TICKET={convs[0].get('ticket_id')}")

    policies = glob.glob("public/policies/*.md")
    print("\n--- Policies ---")
    print(f"Found {len(policies)} policies:")
    for p in policies:
        print(f"  {p}")

    products = glob.glob("public/products/*.md")
    print("\n--- Product Specs ---")
    print(f"Found {len(products)} product specifications:")
    for p in products:
        print(f"  {p}")

if __name__ == "__main__":
    main()
