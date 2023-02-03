from datetime import datetime
from uuid import uuid4

from src.model.deck import Deck


class Game:
    def __init__(
        self, game_id: uuid4 = None, created_at: datetime = None, cards: Deck = None
    ):
        self.id: str = game_id
        self.created_at: datetime = created_at
        self.cards: Deck = cards

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.created_at == other.created_at
            and self.cards == other.cards
        )
