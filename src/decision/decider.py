from typing import List, Dict, Any

class Decider:
    def __init__(self, verifier, policy_engine):
        self.verifier = verifier
        self.policy_engine = policy_engine
        
    def decide(self, customer_id: str, understanding: Any, current_date: Optional[str] = None) -> List[Dict[str, Any]]:
        decisions = []
        verified = self.verifier.verify_request(customer_id, understanding)
        calc_date = current_date or getattr(understanding, "current_date", None)
        
        for intent in understanding.intents:
            move = "ANSWER"
            reason = "general_response"
            policy_ref = "Standard Policy"
            
            # P1: Safety or Legal
            if "safety" in understanding.flags or "legal" in understanding.flags:
                move = "ESCALATE"
                reason = "safety_or_legal"
                policy_ref = "Customer Escalation Policy Section 3"
                
            # P2: Account Suspended
            elif "ACCOUNT_SUSPENDED" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "ACCOUNT_SUSPENDED"
                policy_ref = "Customer Escalation Policy Section 3"
                
            # P3: Human Agent Requested
            elif "human" in understanding.flags or intent == "human_agent":
                move = "ESCALATE"
                reason = "human_requested"
                policy_ref = "Customer Escalation Policy Section 3"
                
            # P4: Ownership / Ambiguity
            elif verified["is_ambiguous"] or (understanding.order_id and not verified["order_exists"]):
                move = "ASK"
                reason = "missing_or_ambiguous_info"
                
            # P5: OTP Dispute on Delivered Orders
            elif "OTP_DISPUTE_LOGISTICS" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "OTP_DISPUTE_LOGISTICS"
                policy_ref = "Shipping Policy Section 5"
                
            # P6: Fraud / Repeated Claims / Contradictions
            elif "REPEATED_CLAIMS" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "REPEATED_CLAIMS"
                policy_ref = "Customer Escalation Policy Section 3"
                
            elif "DIFFERENT_REFUND_DESTINATION" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "DIFFERENT_REFUND_DESTINATION"
                policy_ref = "Payment Policy Section 5"
                
            elif "CONTRADICTION" in verified["risk_signals"]:
                move = "ESCALATE"
                reason = "CONTRADICTION"
                policy_ref = "Customer Escalation Policy Section 3"
                
            # P7: Transactional Actions (Refund, Return, Replacement, Cancellation, Address Change)
            elif intent in ["refund", "return", "cancellation", "replacement", "address_change"]:
                order = verified.get("order_state", {})
                status = str(order.get("status", "")).lower()
                order_date = str(order.get("order_date", "2026-06-01"))
                
                # Check approval threshold (> 75,000 in v2 or > 100,000 in v1)
                is_above_threshold = (
                    "HIGH_VALUE_THRESHOLD" in verified["risk_signals"] or
                    (understanding.amount_claimed and understanding.amount_claimed > 75000)
                )
                
                if intent == "cancellation":
                    if status in ["placed", "confirmed", "processing"]:
                        move = "ACT"
                        reason = "eligible"
                        policy_ref = "Cancellation Policy Section 1"
                    elif status in ["shipped", "out_for_delivery"]:
                        move = "ANSWER"
                        reason = "cancellation_dispatched"
                        policy_ref = "Cancellation Policy Section 1"
                    else:
                        move = "ANSWER"
                        reason = "already_delivered"
                        policy_ref = "Cancellation Policy Section 1"
                        
                elif intent == "address_change":
                    if status in ["placed", "confirmed", "processing"]:
                        move = "ACT"
                        reason = "eligible"
                        policy_ref = "Shipping Policy Section 6"
                    else:
                        move = "ANSWER"
                        reason = "address_change_post_dispatch"
                        policy_ref = "Shipping Policy Section 6"
                        
                elif intent in ["refund", "return", "replacement"]:
                    if is_above_threshold:
                        move = "ESCALATE"
                        reason = "above_threshold"
                        policy_ref = "Refund Policy Section 6"
                    elif str(order.get("payment_status", "")).lower() == "refunded":
                        move = "ANSWER"
                        reason = "already_refunded"
                        policy_ref = "Refund Policy Section 1"
                    else:
                        # Window check if calc_date is explicitly provided
                        is_defect = "damaged" in understanding.flags or "defective" in understanding.flags
                        tier = verified.get("loyalty_tier", "standard")
                        eligible = True
                        pol = {"version": "v2"}
                        if calc_date:
                            try:
                                eligible, pol = self.policy_engine.is_eligible_for_return(order_date, calc_date, loyalty_tier=tier, is_defect=is_defect)
                            except Exception:
                                eligible = True
                                pol = {"version": "v2"}
                            
                        if not eligible:
                            move = "ANSWER"
                            reason = "window_expired"
                            policy_ref = f"Return Policy {pol.get('version', 'v2')} Section 1"
                        elif is_defect and not understanding.evidence_provided:
                            move = "ASK"
                            reason = "evidence_required"
                            policy_ref = "Return Policy Section 4"
                        else:
                            move = "ACT"
                            reason = "eligible"
                            policy_ref = f"Refund Policy {pol.get('version', 'v2')}"
                            
            # P8: Information requests (Status, ETA, Delay, Specs, Policy, Ticket, COD, Payment)
            else:
                move = "ANSWER"
                if intent in ["status", "order_status"]:
                    reason = "order_status"
                elif intent == "delivery_eta":
                    reason = "delivery_eta"
                elif intent == "delivery_delay":
                    reason = "delivery_delay"
                elif intent in ["product_spec", "product_info"]:
                    reason = "product_spec"
                elif "policy" in intent:
                    reason = "policy_information"
                elif intent == "previous_ticket_status":
                    reason = "ticket_status"
                elif intent == "cod_inquiry":
                    reason = "cod_inquiry"
                elif intent in ["payment_pending", "duplicate_payment"]:
                    reason = intent
                else:
                    reason = "general_response"
                    
            decisions.append({
                "intent": intent,
                "move": move,
                "reason_code": reason,
                "policy_ref": policy_ref
            })
            
        return decisions
