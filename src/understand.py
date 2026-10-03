import json
from src.contracts import UnderstandingContract
from src.provider import LLMProvider
from src.entity_resolution import EntityResolver
from pydantic import ValidationError
from typing import Optional, Dict, Any

class LLMUnderstander:
    def __init__(self, provider: LLMProvider, datasets: Optional[Dict[str, Any]] = None):
        self.provider = provider
        self.datasets = datasets
        self.resolver = EntityResolver(datasets)
        
    def set_datasets(self, datasets: Dict[str, Any]):
        self.datasets = datasets
        self.resolver = EntityResolver(datasets)

    def understand(self, message: str, session: Any, customer_id: Optional[str] = None, datasets: Optional[Dict[str, Any]] = None, retries: int = 1) -> UnderstandingContract:
        """Determines customer intent, extracts entities, and performs deterministic entity resolution."""
        if datasets and datasets is not self.datasets:
            self.set_datasets(datasets)

        # Untrusted input wrapper:
        wrapped_prompt = f"<customer_data>\n{message}\n</customer_data>"

        contract = None
        for attempt in range(retries + 1):
            try:
                raw_result = self.provider.call(wrapped_prompt, "SYSTEM_PROMPT")
                contract = UnderstandingContract(**raw_result)
                break
            except (ValidationError, Exception):
                if attempt == retries:
                    contract = UnderstandingContract(intents=["general"], flags=["understanding_failed"])

        if contract is None:
            contract = UnderstandingContract(intents=["general"], flags=["understanding_failed"])

        # Deterministic Entity Resolution step
        # Follows priority: 1. customer, 2. session, 3. message, 4. conv, 5. ticket, 6. orders
        resolved = self.resolver.resolve(customer_id, message, session)

        if resolved.get("ownership_error"):
            # Customer asked about another customer's order
            contract.flags.append("ownership_violation")
            contract.order_id = resolved["order_id"] # Pass for verification to reject safely
        elif resolved.get("order_id"):
            contract.order_id = resolved["order_id"]

        if resolved.get("product_id"):
            contract.product_id = resolved["product_id"]
        if resolved.get("product_name"):
            contract.product_name = resolved["product_name"]
        if resolved.get("category"):
            contract.category = resolved["category"]
        if resolved.get("ticket_id"):
            contract.ticket_id = resolved["ticket_id"]
        if resolved.get("amount_claimed") and not contract.amount_claimed:
            contract.amount_claimed = resolved["amount_claimed"]

        if resolved.get("is_ambiguous"):
            contract.requires_clarification = True
            contract.clarification_prompt = resolved.get("clarification_prompt")
            contract.candidate_matches = resolved.get("candidate_matches", {})
            if "ambiguity" not in contract.intents:
                contract.intents.append("ambiguity")

        return contract
