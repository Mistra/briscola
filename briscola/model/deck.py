import briscola.model.card as card
import random


class Deck():
    cards = []

    def __init__(self):
        self.cards = [
            card.Card(value, suit) for value in card.CardValue for suit in card.CardSuit
        ]
        self.__shuffle()

    def __shuffle(self):
        random.seed(1)
        random.shuffle(self.cards)

    def pick_next(self):
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0
