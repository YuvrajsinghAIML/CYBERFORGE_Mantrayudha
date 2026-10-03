from datetime import datetime
import uuid
import zoneinfo

class ActionLog:
    def __init__(self):
        self.logs = []
        self.tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        
    def record_action(self, action_type, identifiers, context=None):
        action_id = str(uuid.uuid4())
        self.logs.append({
            "action_id": action_id,
            "action_type": action_type,
            "identifiers": identifiers,
            "context": context,
            "timestamp": datetime.now(self.tz).isoformat()
        })
        return action_id
        
    def get_logs(self):
        return self.logs
