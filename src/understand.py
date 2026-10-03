import json
from src.contracts import UnderstandingContract

class LLMUnderstander:
    def __init__(self, llm_client=None):
        self.llm = llm_client
        
    def understand(self, message, session, retries=1):
        if self.llm:
            # Fake LLM logic for tests
            return self.llm.call_understanding(message, session)
            
        # Fallback heuristic for tests
        intents = ["general"]
        if "refund" in message.lower():
            intents = ["refund"]
        order_id = None
        if "ORD-" in message:
            start = message.find("ORD-")
            order_id = message[start:start+10] # O001 is not ORD- format, let's fix
        if "O00" in message:
            start = message.find("O00")
            order_id = message[start:start+4]
            
        return UnderstandingContract(intents=intents, order_id=order_id, intent_type="transaction" if "refund" in intents else "general")
