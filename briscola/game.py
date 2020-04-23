import enum
import random
from datetime import datetime
import time
import string


class CardSuit(enum.Enum):
    HEART = 1
    SPADE = 2
    DIAMOND = 3
    CLUB = 4


class CardValue(enum.Enum):
    DEUCE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    JACK = 6
    QUEEN = 7
    KING = 8
    THREE = 9
    ACE = 10


class Card(tuple):
    def __new__(cls, value, suit):
        assert isinstance(value, CardValue)
        assert isinstance(suit, CardSuit)
        return tuple.__new__(cls, (value, suit))

    @property
    def value(self):
        return self[0]

    @property
    def suit(self):
        return self[1]

    def __str__(self):
        return "{} of {}S".format(self.value.name, self.suit.name)

    def __setattr__(self, *ignored):
        raise NotImplementedError

    def __delattr__(self, *ignored):
        raise NotImplementedError


class Deck():
    def __init__(self):
        self.cards = [
            Card(value, suit) for value in CardValue for suit in CardSuit
        ]

    def shuffle(self):
        random.seed(1)
        random.shuffle(self.cards)


class Game(object):
    def __init__(self, username):
        self.players = []
        self.deck = Deck()
        self.game_id = self.generate_room_id()
        self.date_created = datetime.now()
        self.date_modified = self.date_created
