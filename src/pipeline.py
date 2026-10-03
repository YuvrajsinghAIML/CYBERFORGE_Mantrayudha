from src.contracts import TraceContract
from src.understand import LLMUnderstander
from src.respond import LLMResponder
from src.memory.session import SessionMemory

class Pipeline:
    def __init__(self, tools, verifier, policy_engine, decider, guardrail, llm=None):
        self.tools = tools
        self.verifier = verifier
        self.policy_engine = policy_engine
        self.decider = decider
        self.guardrail = guardrail
        self.understander = LLMUnderstander(llm)
        self.responder = LLMResponder(llm)
        
    def handle_message(self, customer_id, message, now, session=None):
        if not session:
            session = SessionMemory()
            
        session.add_message("customer", message)
        
        # 1. Understand
        understanding = self.understander.understand(message, session)
        
        # Use session memory for missing order
        if not understanding.order_id and session.resolved.get("order_id"):
            understanding.order_id = session.resolved.get("order_id")
            
        if understanding.order_id:
            session.update_resolved("order_id", understanding.order_id)
            
        # 2. Verify
        verified = self.verifier.verify_request(customer_id, understanding)
        
        # 3. Policy & 4. Decide
        decisions = self.decider.decide(customer_id, understanding)
        
        results = []
        for d in decisions:
            if d["move"] == "ACT":
                # Guardrail & Execute
                action_type = "create_" + d["intent"]
                valid, msg = self.guardrail.validate_action(customer_id, action_type, {"order_id": understanding.order_id}, understanding, d)
                if valid:
                    if d["intent"] == "refund":
                        res = self.tools.create_refund(customer_id, understanding.order_id, 0)
                    else:
                        res = self.tools.create_return(customer_id, understanding.order_id)
                    results.append(res)
                else:
                    d["move"] = "ESCALATE"
                    d["reason_code"] = "guardrail_failed"
                    
            if d["move"] == "ASK":
                session.set_pending("need_info")
            else:
                session.set_pending("null")
                
        reply = self.responder.respond(decisions, results, session)
        session.add_message("agent", reply)
        
        trace = TraceContract(
            understanding=understanding,
            verification=verified,
            decisions=decisions,
            tool_calls=results
        )
        
        return reply, decisions, trace, session
