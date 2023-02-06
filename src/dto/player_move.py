from uuid import uuid4

from src.model.card import Card


class PlayerMove:
    def __init__(self, player_id: uuid4 = None, card: Card = None):
        self.player_id: uuid4 = player_id
        self.card: Card = card
