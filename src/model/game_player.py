from uuid import uuid4


class GamePlayer:
    def __init__(
        self,
        game_player_id: uuid4 = None,
        game_id: uuid4 = None,
        player_id: uuid4 = None,
    ):
        self.id: str = game_player_id
        self.game_id: str = game_id
        self.player_id: str = player_id

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.game_id == other.game_id
            and self.player_id == other.player_id
        )
