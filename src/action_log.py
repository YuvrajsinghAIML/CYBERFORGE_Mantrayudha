from datetime import datetime
import uuid
import zoneinfo

class ActionLog:
    def __init__(self):
        self.logs = []
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        
    def record_action(self, action_type, customer_id, identifiers, parameters=None):
        # Idempotency check
        for log in self.logs:
            if log["action_type"] == action_type and log["customer_id"] == customer_id and log["identifiers"] == identifiers:
                return log["action_id"] # Return existing action ID if identical action already performed
                
        action_id = str(uuid.uuid4())
        self.logs.append({
            "action_id": action_id,
            "action_type": action_type,
            "customer_id": customer_id,
            "identifiers": identifiers,
            "parameters": parameters or {},
            "timestamp": datetime.now(self.tz).isoformat()
        })
        return action_id
        
    def get_logs(self):
        return self.logs
