from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any

class UnderstandingContract(BaseModel):
    intents: List[str]
    intent_type: str = "general"
    order_id: Optional[str] = None
    reason: Optional[str] = None
    topic: Optional[str] = None
    amount_claimed: Optional[float] = None
    flags: List[str] = Field(default_factory=list)
    evidence_provided: bool = False
    language: str = "en"
    
    @model_validator(mode='after')
    def check_intents(self) -> 'UnderstandingContract':
        if not self.intents:
            raise ValueError("Intents list cannot be empty")
        valid_intents = {"refund", "return", "cancellation", "status", "escalate", "general", "replacement"}
        for intent in self.intents:
            if intent not in valid_intents:
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
