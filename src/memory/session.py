from typing import Dict, Any, List, Optional

class SessionMemory:
    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.pending: str = "null"
        self.resolved: Dict[str, Any] = {}
        
        # Phase 6 Part 5 context fields
        self.active_order: Optional[str] = None
        self.active_product: Optional[str] = None
        self.active_category: Optional[str] = None
        self.active_intent: Optional[str] = None
        self.pending_clarification: Optional[str] = None
        self.candidate_orders: List[Dict[str, Any]] = []
        self.candidate_products: List[Dict[str, Any]] = []
        self.provided_evidence: List[str] = []
        self.relevant_ticket: Optional[Dict[str, Any]] = None
        self.relevant_previous_answer: Optional[str] = None
        self.unresolved_reason: Optional[str] = None
        
    def update_resolved(self, key: str, value: Any):
        self.resolved[key] = value
        if key == "order_id":
            self.active_order = value
        elif key == "product_id":
            self.active_product = value
        elif key == "category":
            self.active_category = value
        elif key == "intent":
            self.active_intent = value
        
    def set_pending(self, state: str, clarification_msg: Optional[str] = None):
        self.pending = state
        self.pending_clarification = clarification_msg
        
    def set_candidates(self, orders: Optional[List[Dict[str, Any]]] = None, products: Optional[List[Dict[str, Any]]] = None):
        if orders is not None:
            self.candidate_orders = orders
        if products is not None:
            self.candidate_products = products

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def add_evidence(self, evidence_str: str):
        if evidence_str not in self.provided_evidence:
            self.provided_evidence.append(evidence_str)

    def resolve_from_candidates(self, query: str) -> Optional[Dict[str, Any]]:
        """Resolves ambiguity based on candidate match like 'The Sony one' or order ID."""
        q = query.lower()
        # Check order candidates
        if self.candidate_orders:
            for cand in self.candidate_orders:
                oid = cand.get("order_id", "").lower()
                pname = cand.get("product_name", "").lower()
                pbrand = cand.get("brand", "").lower()
                pcat = cand.get("category", "").lower()
                if (oid and oid in q) or (pbrand and pbrand in q) or (pname and any(w in q for w in pname.split())) or (pcat and pcat in q):
                    self.active_order = cand.get("order_id")
                    self.update_resolved("order_id", cand.get("order_id"))
                    self.candidate_orders = []
                    self.pending = "null"
                    self.pending_clarification = None
                    return cand

        # Check product candidates
        if self.candidate_products:
            for cand in self.candidate_products:
                pid = cand.get("product_id", "").lower()
                pname = cand.get("product_name", "").lower()
                pbrand = cand.get("brand", "").lower()
                if (pid and pid in q) or (pbrand and pbrand in q) or (pname and any(w in q for w in pname.split())):
                    self.active_product = cand.get("product_id")
                    self.update_resolved("product_id", cand.get("product_id"))
                    self.candidate_products = []
                    self.pending = "null"
                    self.pending_clarification = None
                    return cand

        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "history": self.history,
            "pending": self.pending,
            "resolved": self.resolved,
            "active_order": self.active_order,
            "active_product": self.active_product,
            "active_category": self.active_category,
            "active_intent": self.active_intent,
            "pending_clarification": self.pending_clarification,
            "candidate_orders": self.candidate_orders,
            "candidate_products": self.candidate_products,
            "provided_evidence": self.provided_evidence,
            "relevant_ticket": self.relevant_ticket,
            "relevant_previous_answer": self.relevant_previous_answer,
            "unresolved_reason": self.unresolved_reason
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMemory':
        sess = cls()
        sess.history = data.get("history", [])
        sess.pending = data.get("pending", "null")
        sess.resolved = data.get("resolved", {})
        sess.active_order = data.get("active_order")
        sess.active_product = data.get("active_product")
        sess.active_category = data.get("active_category")
        sess.active_intent = data.get("active_intent")
        sess.pending_clarification = data.get("pending_clarification")
        sess.candidate_orders = data.get("candidate_orders", [])
        sess.candidate_products = data.get("candidate_products", [])
        sess.provided_evidence = data.get("provided_evidence", [])
        sess.relevant_ticket = data.get("relevant_ticket")
        sess.relevant_previous_answer = data.get("relevant_previous_answer")
        sess.unresolved_reason = data.get("unresolved_reason")
        return sess
