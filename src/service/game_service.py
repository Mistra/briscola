
import logging
import random
from datetime import datetime
from uuid import uuid4 as uuid

from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.won_stack import WonStack


class GameService:
    datetime = None
    id_generator = None
    game_repository = None

    def __init__(self, game_repository=None):
        self.datetime = datetime
        self.id_generator = uuid
        self.game_repository = game_repository

    def create(self, player_ids: list[uuid]):
        logging.debug('Setting up the game for players: %s', player_ids)

        game = Game()

        game.id = str(self.id_generator())

        deck = Deck.init_shuffled()

        # decide player's turn
        random.shuffle(player_ids)

        # create hands for each player
        game.hands = self._create_hands(player_ids, deck)
        game.deck = deck
        game.won_stacks = self._create_won_stacks(player_ids)

        self.game_repository.save(game)

    def fetch_state(self, game_id, player_id):
        # check what's in player's hands
        # check what's player's turn
        # check what's in table
        # check what's in stack
        # check last played hand
        # check deck (number of cards and briscola/last)
        pass

    def _create_won_stacks(self, player_ids: list[uuid]) -> list[WonStack]:
        won_stacks = []
        for player_id in player_ids:
            won_stack = WonStack()

            won_stack.id = str(self.id_generator())
            won_stack.player_id = player_id
            won_stack.cards = []

        return won_stacks

    def _create_hands(self, player_ids: list[uuid], deck: Deck) -> list[Hand]:
        hands = []
        for turn, player_id in enumerate(player_ids):
            hand = Hand()

            hand.id = str(self.id_generator())
            hand.created_at = hand.updated_at = self.datetime.now()
            hand.turn = turn
            hand.player_id = player_id
            hand.cards = deck.pick(3)

        return hands
