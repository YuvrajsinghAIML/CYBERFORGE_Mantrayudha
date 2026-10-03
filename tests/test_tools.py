import pytest
from src.tools import Tools
from src.policy_engine import PolicyEngine
from src.action_log import ActionLog
from db.dataset_loader import load_datasets

def test_tools():
    # Use demo data explicitly instead of skipping
    datasets = load_datasets(use_demo=True)
        
    log = ActionLog()
    pe = PolicyEngine([
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0}
    ])
    tools = Tools(datasets, log, pe)
    
    cust = tools.get_customer("C001")
    assert cust["name"] == "Alice"
    
    order = tools.get_order("C001", "O001")
    assert order["order_id"] == "O001"
    assert len(order["items"]) > 0
    
    with pytest.raises(ValueError):
        tools.get_order("C002", "O001") # Wrong customer
        
    # Idempotency
    res1 = tools.create_return("C001", "O001")
    res2 = tools.create_return("C001", "O001")
    assert res1["action_id"] == res2["action_id"]
    
    # Conversations
    convos = tools.get_conversations("C001")
    assert len(convos["conversations"]) >= 1
