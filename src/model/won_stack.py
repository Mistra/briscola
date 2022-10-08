
from src.model.card import get_card_point


class WonStack():
    id = None
    cards = []
    player_id = None

    def is_empty(self):
        '''Check if the deck is empty'''
        return len(self.cards) == 0

    def calculate_score(self) -> int:
        '''Given the actual stack of cards, calculate the score'''
        return sum(get_card_point(card.value) for card in self.cards)
