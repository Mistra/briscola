from typing import List

from src.model.card import Card, get_card_point


class Stack:
    def __init__(self):
        self.id: str = None
        self.game_id: str = None
        self.player_id: str = None
        self.cards: List[Card] = []

    def is_empty(self):
        """Check if the deck is empty"""
        return len(self.cards) == 0

    def calculate_score(self) -> int:
        """Given the actual stack of cards, calculate the score"""
        return sum(get_card_point(card.value) for card in self.cards)

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.game_id == other.game_id
            and self.player_id == other.player_id
            and self.cards == other.cards
        )
