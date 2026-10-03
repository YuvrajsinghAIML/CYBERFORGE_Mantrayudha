import pytest
from src.policy_engine import PolicyEngine

def test_policy_engine_v1():
    versions = [
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0},
        {"version": "v2", "effective_from": "2026-06-01", "return_window_days": 10, "restocking_fee_percent": 5}
    ]
    pe = PolicyEngine(versions)
    
    # Order before v2 is v1
    policy = pe.get_applicable_policy("2026-05-31")
    assert policy["version"] == "v1"
    
    # Order after v2 is v2
    policy = pe.get_applicable_policy("2026-06-01")
    assert policy["version"] == "v2"

def test_refund_calculation():
    versions = [
        {"version": "v2", "effective_from": "2026-06-01", "return_window_days": 10, "restocking_fee_percent": 5}
    ]
    pe = PolicyEngine(versions)
    policy = pe.get_applicable_policy("2026-06-05")
    
    # Laptop restocking fee
    refund = pe.calculate_refund(100000, "Laptop", policy)
    assert refund == 97500 # 5% of 100k = 5000, max 2500, so refund should be 97500
    
    # Wait, my logic maxes the fee at 2500
    # Let's fix the assertion: 100000 * 0.05 = 5000 -> max 2500 fee -> refund 97500
    assert refund == 97500
    
    # Non-restock category
    refund2 = pe.calculate_refund(100000, "Toy", policy)
    assert refund2 == 100000
