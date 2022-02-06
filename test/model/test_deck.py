

from src.model.card import CardSuit, CardValue
from src.model.deck import Deck


def test_deck_size():
    test_deck = Deck()
    assert len(test_deck.cards) == 40


def test_deck_construction():
    cards = Deck().cards
    assert cards[0].value == CardValue.DEUCE
    assert cards[11].suit == CardSuit.SPADE
    assert cards[22].value == CardValue.FIVE
    assert cards[33].suit == CardSuit.CLUB
