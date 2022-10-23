
class GamePlayer:
    id: None
    game_id: None
    player_id: None

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.game_id == other.game_id and \
            self.player_id == other.player_id
