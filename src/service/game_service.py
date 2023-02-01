import logging
import random
from datetime import datetime
from typing import Optional
from uuid import uuid4 as uuid

from src.dto.game_state import GameState
from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack
from src.repository.game_player_repository import GamePlayerRepository
from src.repository.game_repository import GameRepository
from src.repository.game_state_repository import GameStateRepository
from src.service.bootstrap_utils import BootstrapUtils


class GameService:
    def __init__(
        self,
        game_repository: GameRepository = None,
        game_player_repository: GamePlayerRepository = None,
        game_state_repository: GameStateRepository = None,
    ):
        self.datetime = datetime
        self.id_generator = uuid
        self.random = random
        self.game_repository = game_repository
        self.game_state_repository = game_state_repository
        self.game_player_repository = game_player_repository

    def create(self, player_id: uuid):
        logging.debug("Setting up the game for player: %s", player_id)

        game = Game()
        game.id = str(self.id_generator())
        game.created_at = datetime.utcnow()

        self.game_repository.create(game)

    def join(self, player_id: uuid, game_id: uuid):
        pass

    def bootstrap(self, game_id: uuid, deck: Optional[Deck] = None):
        number_of_players = 2
        game = self.__initialize_game(game_id, deck)
        player_stacks = self.__create_player_stacks(number_of_players, game_id)
        player_hands = self.__create_hands(number_of_players, game.cards, game_id)

        game_state = GameState()
        game_state.game = game
        game_state.player_stacks = player_stacks
        game_state.player_hands = player_hands

        self.game_state_repository.save(game_state)

    def fetch_state(self, game_id):
        pass

    def fetch_state_for_player(self, game_id, player_id):
        # check what's in player's hands
        # check what's player's turn
        # check what's in table
        # check what's in stack
        # check last played hand
        # check deck (number of cards and briscola/last)
        pass

    def __create_player_stacks(
        self, number_of_players: int, game_id: str
    ) -> list[Stack]:
        stacks: list[Stack] = []

        for _ in range(number_of_players):
            stack = Stack()

            stack.id = str(self.id_generator())
            stack.game_id = game_id
            stack.cards = []

            stacks.append(stack)

        return stacks

    def __create_hands(
        self, number_of_players: int, deck: Deck, game_id: str
    ) -> list[Hand]:
        hands: list[Hand] = []
        turns = BootstrapUtils.roll_turn_sequence(number_of_players, self.random)

        for idx in range(number_of_players):
            hand = Hand()

            hand.id = str(self.id_generator())
            hand.updated_at = self.datetime.utcnow()
            hand.game_id = game_id
            hand.turn = turns[idx]
            hand.cards = deck.pick(3)

            hands.append(hand)

        return hands

    def __initialize_game(self, game_id: str, deck: Deck) -> Game:
        game = Game()

        game.id = game_id
        game.cards = Deck.init_shuffled() if deck is None else deck

        return game
