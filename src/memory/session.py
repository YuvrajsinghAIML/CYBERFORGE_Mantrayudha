class SessionMemory:
    def __init__(self):
        self.history = []
        self.pending = "null"
        self.resolved = {}
        
    def update_resolved(self, key, value):
        self.resolved[key] = value
        
    def set_pending(self, state):
        self.pending = state
        
    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
