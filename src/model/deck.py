import random

from src.model.card import Card, CardSuit, CardValue


class Deck:
    def __init__(self, cards=None, rnd=random):
        self.rnd = rnd
        self.cards = (
            [Card(value, suit) for suit in CardSuit for value in CardValue]
            if cards is None
            else cards
        )

    @staticmethod
    def init_shuffled():
        """Returns an initialized and shuffled deck"""
        deck = Deck()
        deck.shuffle()
        return deck

    def shuffle(self):
        """Shuffle the deck"""
        self.rnd.shuffle(self.cards)

    def pick(self, amount: int = 1) -> list[Card]:
        """Pick the next n cards from the deck, if amount is not specified, pick 1"""

        if len(self.cards) < amount:
            raise Exception("Not enough cards in the deck")

        remaining_cards = self.cards[: len(self.cards) - amount]
        picked_cards = self.cards[len(self.cards) - amount :]
        self.cards = remaining_cards

        return picked_cards

    def is_empty(self):
        """Check if the deck is empty"""
        return len(self.cards) == 0

    def __eq__(self, other) -> bool:
        return self.cards == other.cards
