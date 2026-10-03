from src.provider import LLMProvider

class LLMResponder:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def respond(self, decisions, results, session):
        move = decisions[0]["move"]
        
        # Real LLM call for generation would happen here using provider.
        # It must only receive limited context: request, verified facts, policy result, final decision, tools.
        
        if move == "ANSWER":
            return "Here is the information you requested."
        elif move == "ASK":
            return "Could you please provide more information?"
        elif move == "ACT":
            return "I have processed your request successfully."
        elif move == "ESCALATE":
            return "I am escalating this to a human agent. They will get back to you."
        return "How can I help you?"
