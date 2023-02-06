from typing import List

from src.model.card import CardSuit
from src.model.hand import Hand


def calculate_winning_hand(hands: List[Hand], trump_suit: CardSuit) -> Hand:
    """Given a hand of cards, calculate the winning card"""
    if len(hands) == 0:
        raise ValueError("No cards")

    trump_hands = list(filter(lambda hand: hand.played_card == trump_suit, hands))
    winning_suit = (
        trump_hands[0].played_card.suit
        if len(trump_hands) > 0
        else hands[0].played_card.suit
    )

    filtered_hands = filter(lambda hand: hand.played_card.suit == winning_suit, hands)
    return max(filtered_hands, key=lambda hand: hand.played_card.value)


# def calculate_winning_stack(stack_list: List[List[Card]]) -> int:
#     '''Given a pile of cards, calculate the one with the highest score'''
#     return max(range(len(stack_list)), key=lambda i: calculate_stack_score(stack_list[i]))
