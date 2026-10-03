from typing import Optional, Dict, Any, List
from src.contracts import TraceContract
from src.understand import LLMUnderstander
from src.respond import LLMResponder
from src.memory.session import SessionMemory
from src.metrics import MetricsManager
from src.provider import LLMProvider
from src.entity_resolution import EntityResolver
from src.guard import OutputGuard
from src.memory.retrieval import PolicyRetriever, ProductSpecRetriever
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
        self.entity_resolver = EntityResolver(getattr(tools, "datasets", None))
        self.output_guard = OutputGuard()
        self.policy_retriever = PolicyRetriever()
        self.spec_retriever = ProductSpecRetriever()
        
    def handle_message(self, customer_id: str, message: str, now: Optional[str] = None, session: Optional[SessionMemory] = None):
        metrics = MetricsManager()
        
        if not session:
            session = SessionMemory()
            
        session.add_message("customer", message)
        
        # 1. LLM Understanding
        t0 = time.time()
        understanding = self.understander.understand(message, session)
        metrics.record_llm_call((time.time() - t0) * 1000)
        
        # 2. Entity Resolution
        resolved_entities = self.entity_resolver.resolve(customer_id, message, session)
        if resolved_entities.get("order_id") and not understanding.order_id:
            understanding.order_id = resolved_entities["order_id"]
        if resolved_entities.get("product_id") and not getattr(understanding, "product_id", None):
            understanding.product_id = resolved_entities["product_id"]
        if resolved_entities.get("amount_claimed") and not understanding.amount_claimed:
            understanding.amount_claimed = resolved_entities["amount_claimed"]
        if resolved_entities.get("ownership_error"):
            if "not_owned" not in understanding.flags:
                understanding.flags.append("not_owned")
        if resolved_entities.get("is_ambiguous"):
            if "ambiguous" not in understanding.flags:
                understanding.flags.append("ambiguous")
        if resolved_entities.get("clarification_prompt"):
            understanding.clarification_prompt = resolved_entities["clarification_prompt"]

        # Session memory continuity
        if not understanding.order_id and session.resolved.get("order_id"):
            understanding.order_id = session.resolved.get("order_id")
            
        if understanding.order_id:
            session.update_resolved("order_id", understanding.order_id)
            session.active_order = understanding.order_id
            
        # 3. Data Verification
        verified = self.verifier.verify_request(customer_id, understanding)
        
        # 4. Lightweight RAG Retrieval (Policy + Product Specs)
        rag_context = {}
        for intent in understanding.intents:
            if any(k in intent for k in ["policy", "refund", "return", "cancel", "delivery", "shipping", "warranty", "payment"]):
                order_date = verified.get("order_state", {}).get("order_date")
                policy_secs = self.policy_retriever.retrieve_policy_sections(intent, order_date=order_date)
                if policy_secs:
                    rag_context["policy_sections"] = policy_secs
            if intent in ["product_spec", "product_info", "general"] or getattr(understanding, "product_id", None):
                order = verified.get("order_state", {})
                cat = verified.get("category") or order.get("category", "")
                prod_id = getattr(understanding, "product_id", None) or verified.get("product_id")
                prod_spec = self.spec_retriever.retrieve_spec(category=cat, product_id=prod_id, query=message)
                if prod_spec.get("found"):
                    rag_context["product_spec"] = prod_spec

        # 5. Deterministic Decision
        decisions = self.decider.decide(customer_id, understanding)
        
        # 6. Guardrail + Optional Tool Execution
        results = []
        for d in decisions:
            metrics.record_decision(d["move"])
            if d["move"] == "ACT":
                action_type = "create_" + d["intent"]
                valid, msg = self.guardrail.validate_action(customer_id, action_type, {"order_id": understanding.order_id}, understanding, d)
                if valid:
                    t1 = time.time()
                    if d["intent"] == "refund":
                        calc_amt = understanding.amount_claimed or verified.get("order_state", {}).get("total_amount", 0)
                        res = self.tools.create_refund(customer_id, understanding.order_id, calc_amt)
                    elif d["intent"] == "cancellation":
                        res = self.tools.create_cancellation(customer_id, understanding.order_id)
                    elif d["intent"] == "address_change":
                        res = self.tools.update_address(customer_id, understanding.order_id, "New Requested Address")
                    elif d["intent"] == "replacement":
                        res = self.tools.create_replacement(customer_id, understanding.order_id)
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
                
        # 7. Final Response Generation
        t2 = time.time()
        reply = self.responder.respond(
            decisions, results, session,
            understanding=understanding,
            verified=verified,
            rag_context=rag_context
        )
        metrics.record_llm_call((time.time() - t2) * 1000)
        
        # 8. Output Guard Verification
        is_safe, violations = self.output_guard.validate(reply, customer_id, verified, decisions, results)
        if not is_safe:
            reply = self.output_guard.sanitize_or_fallback(reply, customer_id, verified, decisions, results)
            
        session.add_message("agent", reply)
        
        # Enforce exactly <= 2 LLM calls per turn
        assert metrics.metrics["llm_calls"] <= 2, f"LLM calls exceeded limit of 2: {metrics.metrics['llm_calls']}"
        
        trace = TraceContract(
            understanding=understanding,
            verification=verified,
            decisions=decisions,
            tool_calls=results,
            metrics=metrics.finalize()
        )
        
        return reply, decisions, trace, session
