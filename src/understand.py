import json
from src.contracts import UnderstandingContract
from src.provider import LLMProvider
from pydantic import ValidationError

class LLMUnderstander:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def understand(self, message, session, retries=1) -> UnderstandingContract:
        # 1 call logic with 1 retry
        for attempt in range(retries + 1):
            try:
                raw_result = self.provider.call(message, "SYSTEM_PROMPT")
                # Parse and validate with Pydantic
                contract = UnderstandingContract(**raw_result)
                return contract
            except ValidationError:
                if attempt == retries:
                    # Deterministic fallback on total failure
                    return UnderstandingContract(intents=["general"], flags=["understanding_failed"])
        return UnderstandingContract(intents=["general"], flags=["understanding_failed"])
