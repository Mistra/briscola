class GamePlayer:
    def __init__(self):
        self.id: str = None
        self.game_id: str = None
        self.player_id: str = None

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.game_id == other.game_id
            and self.player_id == other.player_id
        )
