from datetime import datetime

from src.model.deck import Deck


class Game:
    def __init__(self):
        self.id: str = None
        self.created_at: datetime = None
        self.cards: Deck = None

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.created_at == other.created_at
            and self.cards == other.cards
        )
