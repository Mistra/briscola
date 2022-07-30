from typing import List

from src.model.card import Card, CardSuit, get_card_point


def calculate_winning_hand(cards: List[Card], trump_suit: CardSuit) -> Card:
    if len(cards) == 0:
        raise ValueError("No cards")

    trump_cards = list(filter(lambda c: c.suit == trump_suit, cards))
    winning_suit = trump_cards[0].suit if len(
        trump_cards) > 0 else cards[0].suit

    filtered_cards = filter(lambda c: c.suit == winning_suit, cards)
    return max(filtered_cards, key=lambda c: c.value)


def calculate_winning_stack(stack_list: List[List[Card]]) -> int:
    return stack_list.index([max(calculate_stack_score(stack)) for stack in stack_list])

# #indices = [index for index, element in enumerate(a_list) if element == [max(calculate_stack_score(stack)) for stack in stack_list]]
# #planets = [['Mercury', 'Venus', 'Earth'], ['Mars', 'Jupiter', 'Saturn'], ['Uranus', 'Neptune', 'Pluto']]
# #flatten_planets = [planet for sublist in planets for planet in sublist if len(planet) < 6]


def calculate_stack_score(stack: List[Card]) -> int:
    return [sum(get_card_point(card.value)) for card in stack]
