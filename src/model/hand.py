

from datetime import datetime
from typing import List

from src.model.card import Card


class Hand():
    id: str
    game_id: str
    player_id: str
    cards: List[Card]
    turn: int = 0
    played_card: Card
    updated_at: datetime

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.game_id == other.game_id and \
            self.player_id == other.player_id and \
            self.cards == other.cards and \
            self.turn == other.turn and \
            self.played_card == other.played_card and \
            self.updated_at == other.updated_at
