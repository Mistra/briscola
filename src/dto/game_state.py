from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack


class GameState:
    def __init__(self):
        self.player_hands: list[Hand] = []
        self.player_stacks: list[Stack] = []
        self.game: Game

    def get_number_of_players(self) -> int:
        len(self.player_hands)

    def __eq__(self, other) -> bool:
        return (
            self.player_hands == other.player_hands
            and self.player_stacks == other.player_stacks
            and self.game == other.game
        )
