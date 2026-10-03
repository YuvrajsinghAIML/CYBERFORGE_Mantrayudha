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
