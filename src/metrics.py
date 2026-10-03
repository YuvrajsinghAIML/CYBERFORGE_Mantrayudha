import time

class MetricsManager:
    def __init__(self):
        self.metrics = {
            "total_latency_ms": 0,
            "llm_latency_ms": 0,
            "tool_latency_ms": 0,
            "llm_calls": 0,
            "tool_calls": 0,
            "escalations": 0,
            "actions": 0,
            "clarifications": 0
        }
        self.start_time = time.time()
        
    def record_llm_call(self, latency_ms):
        self.metrics["llm_calls"] += 1
        self.metrics["llm_latency_ms"] += latency_ms
        
    def record_tool_call(self, latency_ms):
        self.metrics["tool_calls"] += 1
        self.metrics["tool_latency_ms"] += latency_ms
        
    def record_decision(self, move):
        if move == "ESCALATE":
            self.metrics["escalations"] += 1
        elif move == "ACT":
            self.metrics["actions"] += 1
        elif move == "ASK":
            self.metrics["clarifications"] += 1

    def finalize(self):
        self.metrics["total_latency_ms"] = (time.time() - self.start_time) * 1000
        return self.metrics
