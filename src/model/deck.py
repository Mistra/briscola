import random

import src.model.card as card


class Deck():
    cards = []

    def __init__(self):
        self.cards = [
            card.Card(value, suit) for suit in card.CardSuit for value in card.CardValue
        ]

    def shuffle(self):
        '''Shuffle the deck'''
        random.seed(1)
        random.shuffle(self.cards)

    def pick_next(self):
        '''Pick the next card from the deck'''
        return self.cards.pop()

    def is_empty(self):
        '''Check if the deck is empty'''
        return len(self.cards) == 0
