from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from src.model.card import Card


class Hand:
    def __init__(
        self,
        hand_id: uuid4 = None,
        game_id: uuid4 = None,
        player_id: uuid4 = None,
        cards: List[Card] = None,
        turn: int = 0,
        played_card: Optional[Card] = None,
        updated_at: datetime = None,
    ):
        self.id: str = hand_id
        self.game_id: str = game_id
        self.player_id: str = player_id
        self.cards: List[Card] = cards
        self.turn: int = turn
        self.played_card: Optional[Card] = played_card
        self.updated_at: datetime = updated_at

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.game_id == other.game_id
            and self.player_id == other.player_id
            and self.cards == other.cards
            and self.turn == other.turn
            and self.played_card == other.played_card
            and self.updated_at == other.updated_at
        )
