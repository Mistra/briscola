import enum


class CardSuit(enum.IntEnum):
    HEART = 1
    SPADE = 2
    DIAMOND = 3
    CLUB = 4


class CardValue(enum.IntEnum):
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


def get_card_point(card_value: int) -> int:
    match card_value:
        case 6: return 1
        case 7: return 2
        case 8: return 3
        case 9: return 10
        case 10: return 11
        case _: return 0


# class CardPoint(enum.IntEnum):
#     DEUCE = 0
#     FOUR = 0
#     FIVE = 0
#     SIX = 0
#     SEVEN = 0
#     JACK = 1
#     QUEEN = 2
#     KING = 3
#     THREE = 10
#     ACE = 11


class Card():
    value = None
    suit = None

    def __init__(self, value, suit):
        if not isinstance(value, CardValue):
            raise ValueError("value must be a CardValue")
        if not isinstance(suit, CardSuit):
            raise ValueError("suit must be a CardSuit")
        self.value = value
        self.suit = suit

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit
        return False
