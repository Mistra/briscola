
import logging
from datetime import datetime
from uuid import uuid4 as uuid

from src.dto.game_bootstrap import GameBootstrap
from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack


class GameService:
    datetime = None
    id_generator = None
    game_repository = None
    game_state_repository = None

    def __init__(self, game_repository=None, game_state_repository=None):
        self.datetime = datetime
        self.id_generator = uuid
        self.game_repository = game_repository
        self.game_state_repository = game_state_repository

    def create(self, player_id: uuid):
        logging.debug('Setting up the game for player: %s', player_id)

        game = Game()
        game.id = str(self.id_generator())
        game.created_at = datetime.utcnow()
        game.cards = Deck.init_shuffled()

        game_bootstrap = GameBootstrap()
        game_bootstrap.game = game
        game_bootstrap.player_id = player_id

        self.game_state_repository.create(game_bootstrap)

    def join(self, player_id: uuid, game_id: uuid):
        pass

    def fetch_state(self, game_id, player_id):
        # check what's in player's hands
        # check what's player's turn
        # check what's in table
        # check what's in stack
        # check last played hand
        # check deck (number of cards and briscola/last)
        pass

    def _create_won_stacks(self, player_ids: list[uuid]) -> list[Stack]:
        won_stacks = []
        for player_id in player_ids:
            won_stack = Stack()

            won_stack.id = str(self.id_generator())
            won_stack.player_id = player_id
            won_stack.cards = []

        return won_stacks

    def _create_hands(self, player_ids: list[uuid], deck: Deck) -> list[Hand]:
        hands = []
        for turn, player_id in enumerate(player_ids):
            hand = Hand()

            hand.id = str(self.id_generator())
            hand.created_at = hand.updated_at = self.datetime.utcnow()
            hand.turn = turn
            hand.player_id = player_id
            hand.cards = deck.pick(3)

        return hands
