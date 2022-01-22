import briscola.model.card as card
import random


class Deck():
    cards = []

    def __init__(self):
        self.cards = [
            card.Card(value, suit) for suit in card.CardSuit for value in card.CardValue
        ]

    def shuffle(self):
        random.seed(1)
        random.shuffle(self.cards)

    def pick_next(self):
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0
