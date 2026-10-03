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
    datasets = load_datasets(use_demo=True)
    log = ActionLog()
    pe = PolicyEngine([
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0}
    ])
    tools = Tools(datasets, log, pe)
    verifier = Verifier(tools)
    decider = Decider(verifier, pe)
    return decider

def test_decider_otp_dispute(decision_stack):
    decider = decision_stack
    understanding = UnderstandingContract(intents=["refund"], order_id="O001", flags=["not_received"], intent_type="transaction")
    decisions = decider.decide("C001", understanding)
    assert decisions[0]["move"] == "ESCALATE"
    assert decisions[0]["reason_code"] == "OTP_DISPUTE_LOGISTICS"
