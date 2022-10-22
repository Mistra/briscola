from typing import List

from src.model.card import Card, CardSuit


def calculate_winning_hand(cards: List[Card], trump_suit: CardSuit) -> Card:
    '''Given a hand of cards, calculate the winning card'''
    if len(cards) == 0:
        raise ValueError("No cards")

    trump_cards = list(filter(lambda c: c.suit == trump_suit, cards))
    winning_suit = trump_cards[0].suit if len(
        trump_cards) > 0 else cards[0].suit

    filtered_cards = filter(lambda c: c.suit == winning_suit, cards)
    return max(filtered_cards, key=lambda c: c.value)


# def calculate_winning_stack(stack_list: List[List[Card]]) -> int:
#     '''Given a pile of cards, calculate the one with the highest score'''
#     return max(range(len(stack_list)), key=lambda i: calculate_stack_score(stack_list[i]))
