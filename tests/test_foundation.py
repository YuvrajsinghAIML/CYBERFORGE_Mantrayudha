import pytest
from db.dataset_loader import load_datasets
from config.config_loader import load_policies
from src.action_log import ActionLog
from src.contracts import UnderstandingContract, TraceContract
from pydantic import ValidationError

def test_load_datasets():
    datasets = load_datasets()
    assert "customers" in datasets
    assert len(datasets["customers"]) > 0

def test_load_policies():
    policies = load_policies()
    assert "versions" in policies
    assert len(policies["versions"]) > 0
    
def test_action_log():
    log = ActionLog()
    action_id = log.record_action("refund", {"order_id": "O001"})
    assert len(log.get_logs()) == 1
    assert log.get_logs()[0]["action_id"] == action_id
    assert "Asia/Kolkata" in log.get_logs()[0]["timestamp"] or "+" in log.get_logs()[0]["timestamp"]

def test_understanding_contract_valid():
    contract = UnderstandingContract(intents=["refund"], order_id="O001")
    assert contract.intents == ["refund"]

def test_understanding_contract_invalid():
    with pytest.raises(ValidationError):
        UnderstandingContract(intents="not-a-list")
