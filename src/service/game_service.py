
import logging
from datetime import datetime
from uuid import uuid4 as uuid

from src.model.deck import Deck
from src.model.game import Game

# {
#     deck_remaining_card_count: 10,
#     deck_last_card: {...},
#     players_state: [
#         player_id: abc,
#         player_hand: {
#             card_count: 3,
#             cards: [
#                 {...},
#                 {...},
#                 {...}
#             ]
#         },
#         played_card: {...}
#         player_stack_count: 4,
#     ]
# }


class GameState:
    deck_remaining_card_count = None
    deck_last_card = None
    players_state = None


class PlayerState:
    player_id = None
    player_hand = None


class PlayerHand:
    card_count = None
    cards = None
    played_card = None
    player_stack_count = None


class GameService:
    datetime = None
    id_generator = None
    deck_repository = None

    def __init__(self, deck_repository=None):
        self.datetime = datetime
        self.id_generator = uuid

    def create(self, lobby_id):
        # initialize a deck and save it
        game_id = str(self.id_generator())
        created_at = self.datetime.now()
        game = Game(game_id, lobby_id, created_at)
        deck = Deck()
        deck.shuffle()
        # self.game_repository.create(game, deck)

    def fetch_state(self, game_id, player_id):
        # check what's in player's hands
        # check what's player's turn
        # check what's in table
        # check what's in stack
        # check last played hand
        # check deck (number of cards and briscola/last)
        pass

    def check_hand(self, game_id, player_id):
        pass

    def check_table(self, game_id, player_id):
        pass

    def check_stack(self, game_id, player_id):
        pass

    def check_deck(self, game_id, player_id):
        pass

    # def play_card(self, game_id, player_id, card):
    #     if (not is_player_turn(player_id, game_id)):
    #         # raise exception
    #         pass
    #     if (not has_card_in_hand(card, player_id, game_id)):
    #         # raise exception
    #         pass

    #     pass
