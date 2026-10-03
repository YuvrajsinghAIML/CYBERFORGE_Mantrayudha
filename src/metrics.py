class MetricsManager:
    def __init__(self):
        self.metrics = {}
        
    def record(self, key, value):
        self.metrics[key] = value
