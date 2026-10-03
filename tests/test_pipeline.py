import pytest
from src.tools import Tools
from src.policy_engine import PolicyEngine
from src.action_log import ActionLog
from src.decision.verify import Verifier
from src.decision.decider import Decider
from src.decision.guardrail import Guardrail
from src.pipeline import Pipeline
from db.dataset_loader import load_datasets

@pytest.fixture
def pipeline():
    datasets = load_datasets()
    log = ActionLog()
    pe = PolicyEngine([
        {"version": "v1", "effective_from": "2020-01-01", "return_window_days": 15, "restocking_fee_percent": 0}
    ])
    tools = Tools(datasets, log, pe)
    verifier = Verifier(tools)
    decider = Decider(verifier, pe)
    guardrail = Guardrail(tools)
    return Pipeline(tools, verifier, pe, decider, guardrail)

def test_pipeline_ask(pipeline):
    reply, decisions, trace, session = pipeline.handle_message("C001", "I need a refund", "2026-06-10")
    assert decisions[0]["move"] == "ASK"
    assert session.pending == "need_info"

def test_pipeline_act_with_memory(pipeline):
    # First turn
    reply, decisions, trace, session = pipeline.handle_message("C001", "I need a refund", "2026-06-10")
    assert decisions[0]["move"] == "ASK"
    
    # Second turn
    reply, decisions, trace, session = pipeline.handle_message("C001", "refund for order O001", "2026-06-10", session)
    assert trace.understanding.order_id == "O001"
    assert decisions[0]["move"] == "ACT"
