import os
import json
import time
from typing import Dict, Any, Optional

class LLMProvider:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        
    def call(self, prompt: str, system: str, retries: int = 1) -> Dict[str, Any]:
        start_time = time.time()
        
        if self.provider == "mock" or not self.api_key:
            return self._mock_call(prompt)
            
        # Place real SDK logic here
        # e.g., OpenAI or Anthropic call
        
        return self._mock_call(prompt)
        
    def _mock_call(self, prompt: str) -> Dict[str, Any]:
        # Deterministic mock logic based on prompt keywords for testing
        p = prompt.lower()
        intents = ["general"]
        if "refund" in p:
            intents = ["refund"]
        elif "status" in p:
            intents = ["status"]
        
        order_id = None
        if "ord-" in p:
            start = p.find("ord-")
            order_id = prompt[start:start+10]
        if "o00" in p:
            start = p.find("o00")
            order_id = prompt[start:start+4].upper()
            
        flags = []
        if "safety" in p or "fire" in p:
            flags.append("safety")
        if "lawyer" in p or "sue" in p:
            flags.append("legal")
        if "human" in p:
            flags.append("human")
        if "ignore previous instructions" in p or "system message" in p:
            flags.append("injection_attempt")
            
        return {
            "intents": intents,
            "intent_type": "transaction" if "refund" in intents else "general",
            "order_id": order_id,
            "flags": flags,
            "raw": '{"intents": ["general"]}'
        }
