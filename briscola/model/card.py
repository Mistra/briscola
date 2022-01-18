import enum


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


class Card():
    value = None
    suit = None

    def __new__(cls, value, suit):
        if isinstance(value, CardValue):
            raise ValueError("value must be a CardValue")
        if isinstance(suit, CardSuit):
            raise ValueError("suit must be a CardSuit")
        cls.value = value
        cls.suit = suit
