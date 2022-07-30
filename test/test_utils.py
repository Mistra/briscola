from src.model.card import Card, CardSuit, CardValue
from src.util import calculate_stack_score, calculate_winning_hand


def test_calculate_winning_hand():
    cards = [Card(CardValue.DEUCE, CardSuit.CLUB),
             Card(CardValue.THREE, CardSuit.CLUB),
             Card(CardValue.DEUCE, CardSuit.DIAMOND),
             Card(CardValue.DEUCE, CardSuit.SPADE)]

    trump_suit = CardSuit.CLUB
    winning_card = cards[1]
    assert calculate_winning_hand(cards, trump_suit) == winning_card

    trump_suit = CardSuit.DIAMOND
    winning_card = cards[2]
    assert calculate_winning_hand(cards, trump_suit) == winning_card


def test_calculate_stack_score():
    cards = [Card(CardValue.JACK, CardSuit.CLUB),
             Card(CardValue.THREE, CardSuit.CLUB),
             Card(CardValue.DEUCE, CardSuit.DIAMOND),
             Card(CardValue.FIVE, CardSuit.SPADE)]
    score = 11
    assert calculate_stack_score(cards) == score
