from src.contracts import TraceContract
from src.understand import LLMUnderstander
from src.respond import LLMResponder
from src.memory.session import SessionMemory
from src.metrics import MetricsManager
from src.provider import LLMProvider
import time

class Pipeline:
    def __init__(self, tools, verifier, policy_engine, decider, guardrail):
        self.tools = tools
        self.verifier = verifier
        self.policy_engine = policy_engine
        self.decider = decider
        self.guardrail = guardrail
        
        self.provider = LLMProvider()
        self.understander = LLMUnderstander(self.provider)
        self.responder = LLMResponder(self.provider)
        
    def handle_message(self, customer_id, message, now, session=None):
        metrics = MetricsManager()
        
        if not session:
            session = SessionMemory()
            
        session.add_message("customer", message)
        
        t0 = time.time()
        understanding = self.understander.understand(message, session)
        metrics.record_llm_call((time.time() - t0) * 1000)
        
        if not understanding.order_id and session.resolved.get("order_id"):
            understanding.order_id = session.resolved.get("order_id")
            
        if understanding.order_id:
            session.update_resolved("order_id", understanding.order_id)
            
        verified = self.verifier.verify_request(customer_id, understanding)
        decisions = self.decider.decide(customer_id, understanding)
        
        results = []
        for d in decisions:
            metrics.record_decision(d["move"])
            if d["move"] == "ACT":
                action_type = "create_" + d["intent"]
                valid, msg = self.guardrail.validate_action(customer_id, action_type, {"order_id": understanding.order_id}, understanding, d)
                if valid:
                    t1 = time.time()
                    if d["intent"] == "refund":
                        res = self.tools.create_refund(customer_id, understanding.order_id, 0)
                    else:
                        res = self.tools.create_return(customer_id, understanding.order_id)
                    metrics.record_tool_call((time.time() - t1) * 1000)
                    results.append(res)
                else:
                    d["move"] = "ESCALATE"
                    d["reason_code"] = "guardrail_failed"
                    metrics.metrics["escalations"] += 1
                    
            if d["move"] == "ASK":
                session.set_pending("need_info")
            else:
                session.set_pending("null")
                
        t2 = time.time()
        reply = self.responder.respond(decisions, results, session)
        metrics.record_llm_call((time.time() - t2) * 1000)
        
        session.add_message("agent", reply)
        
        # Enforce exactly <= 2 LLM calls
        assert metrics.metrics["llm_calls"] <= 2, "LLM calls exceeded limit of 2"
        
        trace = TraceContract(
            understanding=understanding,
            verification=verified,
            decisions=decisions,
            tool_calls=results,
            metrics=metrics.finalize()
        )
        
        return reply, decisions, trace, session
