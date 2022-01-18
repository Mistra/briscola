import datetime


class Lobby():
    id = None
    player_ids = None
    created_at = None
    last_activity_at = None

    def __init__(self):
        self.created_at = datetime.now()
