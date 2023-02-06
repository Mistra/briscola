from typing import List, Optional
from uuid import uuid4

from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack


class GameState:
    def __init__(
        self,
        player_hands: List[Hand] = None,
        player_stacks: List[Stack] = None,
        game: Optional[Game] = None,
    ):
        self.player_hands: list[Hand] = player_hands
        self.player_stacks: list[Stack] = player_stacks
        self.game: Optional[Game] = game

    def get_number_of_players(self) -> int:
        len(self.player_hands)

    def get_player_hand(self, player_id: uuid4) -> Hand:
        return next(
            (hand for hand in self.player_hands if hand.player_id == player_id),
            None,
        )

    def get_player_stack(self, player_id: uuid4) -> Stack:
        return next(
            (stack for stack in self.player_stacks if stack.player_id == player_id),
            None,
        )

    def __eq__(self, other) -> bool:
        return (
            self.player_hands == other.player_hands
            and self.player_stacks == other.player_stacks
            and self.game == other.game
        )
