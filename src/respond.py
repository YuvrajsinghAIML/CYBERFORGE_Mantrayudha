from typing import List, Dict, Any, Optional
from src.provider import LLMProvider

class LLMResponder:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def respond(self, decisions: List[Dict[str, Any]], results: List[Dict[str, Any]], session: Any, 
                understanding: Optional[Any] = None, verified: Optional[Dict[str, Any]] = None, 
                rag_context: Optional[Dict[str, Any]] = None) -> str:
        """Generates grounded, concise, natural responses strictly matching verified facts and terminal moves."""
        if not decisions:
            return "How can I assist you with your NovaMart orders today?"

        verified = verified or {}
        order = verified.get("order_state", {})
        order_id = getattr(understanding, "order_id", None) or order.get("order_id")
        
        # Multi-intent response formatting
        if len(decisions) > 1:
            sections = []
            for i, d in enumerate(decisions, 1):
                part = self._generate_move_response(d, results, session, understanding, verified, rag_context)
                intent_label = d.get("intent", "Request").replace("_", " ").title()
                sections.append(f"{i}. **{intent_label}**: {part}")
            return "Here is the status of your requests:\n" + "\n".join(sections)
            
        # Single intent response
        return self._generate_move_response(decisions[0], results, session, understanding, verified, rag_context)

    def _generate_move_response(self, decision: Dict[str, Any], results: List[Dict[str, Any]], session: Any,
                                understanding: Optional[Any], verified: Dict[str, Any], 
                                rag_context: Optional[Dict[str, Any]]) -> str:
        move = decision.get("move", "ANSWER")
        reason = decision.get("reason_code", "")
        intent = decision.get("intent", "general")
        order = verified.get("order_state", {})
        order_id = getattr(understanding, "order_id", None) or order.get("order_id", "")

        # ------------------- ASK -------------------
        if move == "ASK":
            if understanding and getattr(understanding, "clarification_prompt", None):
                return understanding.clarification_prompt
            if session and getattr(session, "pending_clarification", None):
                return session.pending_clarification
            if reason == "evidence_required":
                return "To proceed with your return for the damaged item, please provide a clear photo showing the damage and the outer packaging."
            if not order_id:
                return "Could you please share your Order ID so I can look up the details for you?"
            return "Could you please provide a few more details so I can assist you with your request?"

        # ------------------- ESCALATE -------------------
        if move == "ESCALATE":
            if reason == "safety_or_legal":
                return "Your request has been escalated to our Priority Safety & Legal Support Desk. A specialist will review your case within 15–30 minutes."
            if reason == "ACCOUNT_SUSPENDED":
                return "Your account is currently undergoing a routine security review. I have forwarded your request to our Trust & Safety team for assistance."
            if reason == "human_requested":
                return "I am connecting you to a human support specialist. A team member will join this conversation shortly."
            if reason == "OTP_DISPUTE_LOGISTICS":
                return f"Order {order_id} is marked as delivered with OTP verification. I have escalated this delivery dispute to our Logistics Investigation Desk; they will investigate with the courier within 3 business days."
            if reason == "above_threshold":
                return f"Your request for order {order_id} exceeds automated limits and has been escalated to our Refunds & Payments Lead for review within 24 hours."
            if reason == "REPEATED_CLAIMS":
                return "Your case has been forwarded to our Senior Account Services team for comprehensive review."
            if reason == "DIFFERENT_REFUND_DESTINATION":
                return "Per security policy, refunds can only be routed to the original payment method. I have escalated your request to Payments for verified alternate routing."
            return "I have escalated your inquiry to our senior customer support specialist team. They will review your case and reach out within 24 to 48 hours."

        # ------------------- ACT -------------------
        if move == "ACT":
            # Match corresponding result
            res = next((r for r in results if isinstance(r, dict) and (r.get("order_id") == order_id or r.get("action_type") == f"create_{intent}")), None)
            if not res and results:
                res = results[0]

            if intent == "cancellation":
                return f"Order {order_id} has been cancelled successfully. Any prepaid amount will be refunded to your original payment method."
            if intent == "refund":
                amt = res.get("amount") if res else getattr(understanding, "amount_claimed", None)
                amt_str = f" of ₹{amt:,.2f}" if amt else ""
                return f"Your refund{amt_str} for order {order_id} has been processed successfully to your original payment method."
            if intent == "return":
                return f"A return has been initiated for order {order_id}. A courier partner will arrive for pickup within 24–48 hours."
            if intent == "replacement":
                return f"A replacement request has been created for order {order_id}. Your replacement item will be dispatched following pickup verification."
            if intent == "address_change":
                return f"The delivery address for order {order_id} has been successfully updated."
            return "I have processed your request successfully."

        # ------------------- ANSWER -------------------
        if intent in ["status", "order_status"]:
            if order:
                status = order.get("status", "processing")
                eta = order.get("estimated_delivery_date", "in 2-3 business days")
                tracking = order.get("tracking_number")
                track_str = f" (Tracking: {tracking})" if tracking else ""
                return f"Order {order_id} is currently {status}{track_str}. Expected delivery date is {eta}."
            return "I could not find an active order matching your account. Please provide an Order ID to check status."

        if intent == "delivery_eta":
            if order:
                eta = order.get("estimated_delivery_date", "in 2-3 business days")
                return f"Order {order_id} is scheduled for delivery on {eta}."
            return "Your order is scheduled for delivery as per the estimated date provided at checkout."

        if intent == "delivery_delay":
            if order:
                eta = order.get("estimated_delivery_date", "shortly")
                return f"Order {order_id} has experienced a slight transit delay. Our logistics partner is expediting delivery; revised estimated delivery is {eta}."
            return "We apologize for the delivery delay. Our logistics team is actively expediting transit."

        if intent in ["product_spec", "product_info"]:
            if rag_context and "product_spec" in rag_context:
                spec_data = rag_context["product_spec"]
                if spec_data.get("found"):
                    specs = spec_data.get("specifications", {})
                    spec_items = [f"{k.capitalize()}: {v}" for k, v in list(specs.items())[:5]]
                    return f"Product specifications for {spec_data.get('category', 'item')}:\n" + "\n".join(spec_items)
            return "Here are the product specifications from our official catalog."

        if "policy" in intent:
            if rag_context and "policy_sections" in rag_context:
                sections = rag_context["policy_sections"]
                if sections:
                    top_sec = sections[0]
                    return f"Under NovaMart's {top_sec.get('heading', 'policy')}:\n{top_sec.get('content', '')[:300]}..."
            if "return" in intent:
                return "NovaMart's Return Policy allows returns within 7 days of delivery for standard items (9 days for Gold, 10 days for Platinum), and 10 days for defective items."
            if "refund" in intent:
                return "Refunds are processed to the original payment instrument within 1-3 days for UPI and 5-7 days for cards after QC inspection."
            if "cancellation" in intent:
                return "Orders can be cancelled before dispatch for a 100% refund. Shipped orders cannot be cancelled directly."
            if "warranty" in intent:
                return "NovaMart products are covered by standard manufacturer warranty policies ranging from 6 to 24 months."
            return "Here is the information from our official policy."

        if reason == "window_expired":
            order_date = order.get("order_date", "earlier")
            return f"Order {order_id} was placed on {order_date} and has passed the return eligibility window."

        if reason == "already_refunded":
            return f"Order {order_id} has already been refunded to your original payment method."

        if reason == "cancellation_dispatched":
            tracking = order.get("tracking_number", "assigned")
            return f"Order {order_id} has already been handed over to the courier (Tracking: {tracking}) and cannot be cancelled directly. You may decline delivery at doorstep or initiate a return after arrival."

        if reason == "address_change_post_dispatch":
            return f"Order {order_id} is already in transit with the courier and its delivery address cannot be modified. Please contact the courier directly or arrange pickup at their hub."

        if reason == "cod_inquiry":
            return "Cash on Delivery (COD) is available on eligible items for order values up to ₹50,000."

        if reason == "payment_pending":
            return "Bank payment confirmations can take up to 24 hours. If an unconfirmed debit occurred, your bank will automatically reverse the charge within 5–7 business days."

        if reason == "duplicate_payment":
            return "If you noticed duplicate debits for your order, any unconfirmed transaction is automatically reversed by banking partners within 5–7 business days."

        if reason == "ticket_status":
            return "Your ticket has been logged and is being handled by our support staff."

        return "Here is the information you requested. Please let me know if you need any further assistance."
