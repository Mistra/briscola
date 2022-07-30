
class Game():
    id = None
    lobby_id = None
    created_at = None

    def __init__(self, id, lobby_id, created_at=None):
        self.id = id
        self.lobby_id = lobby_id
        self.created_at = created_at
