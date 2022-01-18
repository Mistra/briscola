from cgi import test
import pytest
from briscola import deck


def test_deck():
    test_deck = Deck()
    assert test_deck.size == 40
    assert test_deck
