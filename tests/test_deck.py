from traceback import print_list
from briscola.model.deck import Deck
from briscola.model.card import Card, CardSuit, CardValue


def test_deck_size():
    test_deck = Deck()
    assert len(test_deck.cards) == 40


def test_deck_construction():
    cards = Deck().cards
    assert (cards[0].value == CardValue.DEUCE)
    assert (cards[11].suit == CardSuit.SPADE)
    assert (cards[22].value == CardValue.FIVE)
    assert (cards[33].suit == CardSuit.CLUB)
