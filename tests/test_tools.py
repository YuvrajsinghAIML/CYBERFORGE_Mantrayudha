from tests.conftest import GLOBAL_C001, GLOBAL_C002, GLOBAL_C003, GLOBAL_O001, GLOBAL_O002, GLOBAL_O003, GLOBAL_P001, GLOBAL_T001, GLOBAL_CONV001
import pytest
from src.tools import Tools
from src.policy_engine import PolicyEngine
from src.action_log import ActionLog
from db.dataset_loader import load_datasets

def test_tools():
    # Use demo data explicitly instead of skipping
    datasets = load_datasets()
        
    log = ActionLog()
    pe = PolicyEngine([
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0}
    ])
    tools = Tools(datasets, log, pe)
    
    cust = tools.get_customer(GLOBAL_C001)
    assert cust["first_name"] is not None
    
    order = tools.get_order(GLOBAL_C001, GLOBAL_O001)
    assert order["order_id"] == GLOBAL_O001
    assert len(order["items"]) > 0
    
    with pytest.raises(ValueError):
        tools.get_order(GLOBAL_C002, GLOBAL_O001) # Wrong customer
        
    # Idempotency
    res1 = tools.create_return(GLOBAL_C001, GLOBAL_O001)
    res2 = tools.create_return(GLOBAL_C001, GLOBAL_O001)
    assert res1["action_id"] == res2["action_id"]
    
    # Conversations
    convos = tools.get_conversations(GLOBAL_C001)
    assert isinstance(convos["conversations"], list)
