

from datetime import datetime

from src.model.deck import Deck


class Game():
    id: str
    created_at: datetime
    cards: Deck

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.created_at == other.created_at and \
            self.cards == other.cards
