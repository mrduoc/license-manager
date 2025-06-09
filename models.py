from datetime import datetime

class License:
    def __init__(self, pc_id, key, active=True, expires=None):
        self.pc_id = pc_id
        self.key = key
        self.active = active
        self.expires = expires
        self.created_at = datetime.now()
