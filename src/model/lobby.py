from datetime import datetime


class Lobby():
    id = None
    player_ids = []
    created_at = None
    last_activity_at = None

    def __init__(self, id, created_at=None, last_activity_at=None):
        self.id = id
        self.created_at = created_at
        self.last_activity_at = last_activity_at

    def add_player(self, player_id):
        self.player_ids.append(player_id)
