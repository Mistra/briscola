# from src.model.card import Card, CardSuit, CardValue
# from src.util import (calculate_stack_score, calculate_winning_hand,
#                       calculate_winning_stack)


# def test_calculate_winning_hand():
#     cards = [Card(CardValue.DEUCE, CardSuit.CLUB),
#              Card(CardValue.THREE, CardSuit.CLUB),
#              Card(CardValue.DEUCE, CardSuit.DIAMOND),
#              Card(CardValue.DEUCE, CardSuit.SPADE)]

#     trump_suit = CardSuit.CLUB
#     winning_card = cards[1]
#     assert calculate_winning_hand(cards, trump_suit) == winning_card

#     trump_suit = CardSuit.DIAMOND
#     winning_card = cards[2]
#     assert calculate_winning_hand(cards, trump_suit) == winning_card


# def test_calculate_stack_score():
#     cards = [Card(CardValue.JACK, CardSuit.CLUB),
#              Card(CardValue.THREE, CardSuit.CLUB),
#              Card(CardValue.DEUCE, CardSuit.DIAMOND),
#              Card(CardValue.FIVE, CardSuit.SPADE)]
#     score = 11
#     assert calculate_stack_score(cards) == score

#     cards = [Card(CardValue.JACK, CardSuit.CLUB),
#              Card(CardValue.ACE, CardSuit.CLUB),
#              Card(CardValue.KING, CardSuit.DIAMOND),
#              Card(CardValue.FIVE, CardSuit.SPADE)]
#     score = 15
#     assert calculate_stack_score(cards) == score


# def test_calculate_winning_stack():
#     stack1 = [Card(CardValue.JACK, CardSuit.CLUB),
#               Card(CardValue.ACE, CardSuit.CLUB)]

#     stack2 = [Card(CardValue.DEUCE, CardSuit.CLUB),
#               Card(CardValue.THREE, CardSuit.CLUB)]

#     stacks = [stack2, stack1]
#     winning_stack = 1
#     assert calculate_winning_stack(stacks) == winning_stack
