

from datetime import datetime

from src.model.deck import Deck


class Game():
    id: str
    created_at: datetime
    deck: Deck

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.created_at == other.created_at and \
            self.deck == other.deck
