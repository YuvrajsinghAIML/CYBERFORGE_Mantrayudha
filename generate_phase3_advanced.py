import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('src/decision/verify.py', """
class Verifier:
    def __init__(self, tools):
        self.tools = tools
        
    def verify_request(self, customer_id, understanding):
        results = {
            "is_valid_customer": False,
            "order_exists": False,
            "is_ambiguous": False,
            "risk_signals": [],
            "contradictions": [],
            "customer_status": "active",
            "order_state": {}
        }
        try:
            cust = self.tools.get_customer(customer_id)
            results["is_valid_customer"] = True
            results["customer_status"] = cust.get("status", "active")
        except ValueError:
            return results
            
        if results["customer_status"] == "suspended":
            results["risk_signals"].append("ACCOUNT_SUSPENDED")
            
        order_id = understanding.order_id
        if order_id:
            try:
                order = self.tools.get_order(customer_id, order_id)
                results["order_exists"] = True
                results["order_state"] = order
                
                # Check Delivery Contradictions
                # Delivered + OTP verified + customer says "not received" -> ESCALATE to Logistics
                if order.get("delivery_status") == "delivered" and "not_received" in understanding.flags:
                    results["risk_signals"].append("OTP_DISPUTE_LOGISTICS")
                    
                # Other contradictions
                if "fraud" in understanding.flags:
                    results["contradictions"].append("SUSPICIOUS_FLAGS")
                    results["risk_signals"].append("CONTRADICTION")
                    
            except ValueError:
                results["is_ambiguous"] = True
        elif understanding.intent_type != "general":
            results["is_ambiguous"] = True
            
        return results
""")

write_file('src/decision/decider.py', """
class Decider:
    def __init__(self, verifier, policy_engine):
        self.verifier = verifier
        self.policy_engine = policy_engine
        
    def decide(self, customer_id, understanding):
        decisions = []
        verified = self.verifier.verify_request(customer_id, understanding)
        
        for intent in understanding.intents:
            move = "ANSWER"
            reason = "general_response"
            
            # P1: Safety
            if "safety" in understanding.flags or "legal" in understanding.flags:
                move = "ESCALATE"
                reason = "safety_or_legal"
            # P2: Suspended
            elif "ACCOUNT_SUSPENDED" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "ACCOUNT_SUSPENDED"
            # P3: Human
            elif "human" in understanding.flags:
                move = "ESCALATE"
                reason = "human_requested"
            # P4/P5: Ambiguity/Not Owned
            elif verified["is_ambiguous"] or (understanding.order_id and not verified["order_exists"]):
                move = "ASK"
                reason = "missing_or_ambiguous_info"
            # P6: OTP Dispute
            elif "OTP_DISPUTE_LOGISTICS" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "OTP_DISPUTE_LOGISTICS"
            # P7: Risks
            elif verified["risk_signals"]:
                move = "ESCALATE"
                reason = verified["risk_signals"][0]
            # P9/P10/P11
            else:
                if intent in ["refund", "return", "cancellation", "replacement"]:
                    # Placeholder check for ACT/ANSWER based on threshold/eligibility
                    if understanding.amount_claimed and understanding.amount_claimed > 75000:
                        move = "ESCALATE"
                        reason = "above_threshold"
                    else:
                        move = "ACT"
                        reason = "eligible"
                        
            decisions.append({
                "intent": intent,
                "move": move,
                "reason_code": reason,
                "policy_ref": "Standard Policy"
            })
            
        return decisions
""")

write_file('tests/test_decision_advanced.py', """
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
""")
