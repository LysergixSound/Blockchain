import json

class BlockModel:
    def __init__(self, previous_hash, public_id, message, signature):
        self.previous_hash = previous_hash
        self.public_id = public_id
        self.message = message
        self.signature = signature
        self.proof = 0
        self.difficulty = 0

    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)
