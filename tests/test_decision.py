from tests.conftest import GLOBAL_C001, GLOBAL_C002, GLOBAL_C003, GLOBAL_O001, GLOBAL_O002, GLOBAL_O003, GLOBAL_P001, GLOBAL_T001, GLOBAL_CONV001
import pytest
from src.tools import Tools
from src.policy_engine import PolicyEngine
from src.action_log import ActionLog
from src.contracts import UnderstandingContract
from src.decision.verify import Verifier
from src.decision.decider import Decider
from src.decision.guardrail import Guardrail
from db.dataset_loader import load_datasets

@pytest.fixture
def decision_stack():
    datasets = load_datasets()
    log = ActionLog()
    pe = PolicyEngine([
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0}
    ])
    tools = Tools(datasets, log, pe)
    verifier = Verifier(tools)
    decider = Decider(verifier, pe)
    guardrail = Guardrail(tools)
    return tools, verifier, decider, guardrail

def test_decider_priority_safety(decision_stack):
    _, _, decider, _ = decision_stack
    understanding = UnderstandingContract(intents=["refund"], order_id=GLOBAL_O001, flags=["safety"])
    decisions = decider.decide(GLOBAL_C001, understanding)
    assert decisions[0]["move"] == "ESCALATE"
    assert decisions[0]["reason_code"] == "safety_or_legal"

def test_decider_priority_suspended(decision_stack):
    _, _, decider, _ = decision_stack
    # C003 is suspended
    understanding = UnderstandingContract(intents=["refund"], order_id=GLOBAL_O001)
    decisions = decider.decide(GLOBAL_C003, understanding)
    assert decisions[0]["move"] == "ESCALATE"
    assert decisions[0]["reason_code"] == "ACCOUNT_SUSPENDED"

def test_decider_ambiguity(decision_stack):
    _, _, decider, _ = decision_stack
    # No order_id specified
    understanding = UnderstandingContract(intents=["refund"], intent_type="transaction")
    decisions = decider.decide(GLOBAL_C001, understanding)
    assert decisions[0]["move"] == "ASK"
    assert decisions[0]["reason_code"] == "missing_or_ambiguous_info"

def test_guardrail(decision_stack):
    tools, _, _, guardrail = decision_stack
    understanding = UnderstandingContract(intents=["refund"], order_id=GLOBAL_O001)
    decision = {"move": "ACT"}
    valid, msg = guardrail.validate_action(GLOBAL_C001, "create_refund", {"order_id": GLOBAL_O001}, understanding, decision)
    assert valid is True
    
    valid, msg = guardrail.validate_action(GLOBAL_C002, "create_refund", {"order_id": GLOBAL_O001}, understanding, decision)
    assert valid is False
