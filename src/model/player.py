

class Player:
    id: None
    name: None
    created_at: None
    last_seen: None

    def __init__(self, id, name, created_at=None, last_seen=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.last_seen = last_seen
