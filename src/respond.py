class LLMResponder:
    def __init__(self, llm_client=None):
        self.llm = llm_client
        
    def respond(self, decisions, results, session):
        if self.llm:
            return self.llm.call_respond(decisions, results, session)
        
        move = decisions[0]["move"]
        if move == "ANSWER":
            return "Here is the information you requested."
        elif move == "ASK":
            return "Could you please provide more information?"
        elif move == "ACT":
            return "I have processed your request successfully."
        elif move == "ESCALATE":
            return "I am escalating this to a human agent. They will get back to you."
        return "How can I help you?"
