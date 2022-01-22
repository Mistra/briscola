from datetime import datetime


class Lobby():
    id = None
    player_ids = None
    created_at = None
    last_activity_at = None

    def __init__(self, id):
        self.id = id
        self.created_at = datetime.now()

    def __init__(self):
        self.created_at = datetime.now()

    def add_player(self, player_id):
        self.player_ids.append(player_id)

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'last_activity_at': self.last_activity_at,
            'player_ids': self.player_ids
        }
