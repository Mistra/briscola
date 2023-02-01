from datetime import datetime
from typing import List, Optional

from src.model.card import Card


class Hand:
    def __init__(self):
        self.id: str = None
        self.game_id: str = None
        self.player_id: str = None
        self.cards: List[Card]
        self.turn: int = 0
        self.played_card: Optional[Card] = None
        self.updated_at: datetime = None

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
