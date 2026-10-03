from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any

VALID_INTENTS = {
    # Foundational / legacy
    "refund", "return", "cancellation", "status", "escalate", "general", "replacement",
    # Phase 6 & 7 detailed intents
    "order_status", "delivery_eta", "delivery_delay", "non_delivery",
    "cancellation_request", "address_change", "return_request", "replacement_request",
    "refund_request", "refund_status", "warranty", "warranty_claim",
    "damaged_item", "wrong_item", "missing_item",
    "product_info", "product_spec", "product_information", "product_specification",
    "payment_pending", "duplicate_payment", "cod_inquiry", "cod_questions",
    "return_policy", "refund_policy", "warranty_policy", "shipping_policy", "cancellation_policy",
    "previous_ticket_status", "previous_conversation_followup", "human_agent",
    "ambiguity", "multi_intent", "unsupported_request", "unsupported"
}

class UnderstandingContract(BaseModel):
    intents: List[str]
    intent_type: str = "general"
    order_id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    ticket_id: Optional[str] = None
    conversation_id: Optional[str] = None
    reason: Optional[str] = None
    topic: Optional[str] = None
    amount_claimed: Optional[float] = None
    new_address: Optional[str] = None
    flags: List[str] = Field(default_factory=list)
    evidence_provided: bool = False
    language: str = "en"
    candidate_matches: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    entities: Dict[str, Any] = Field(default_factory=dict)
    requires_clarification: bool = False
    clarification_prompt: Optional[str] = None
    untrusted_input_sanitized: Optional[str] = None
    
    @model_validator(mode='after')
    def check_intents(self) -> 'UnderstandingContract':
        if not self.intents:
            raise ValueError("Intents list cannot be empty")
        for intent in self.intents:
            if intent not in VALID_INTENTS:
                raise ValueError(f"Invalid intent: {intent}")
        return self

class TraceContract(BaseModel):
    understanding: UnderstandingContract
    verification: Dict[str, Any] = Field(default_factory=dict)
    policy: Dict[str, Any] = Field(default_factory=dict)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    guard: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    rag_context: Dict[str, Any] = Field(default_factory=dict)
