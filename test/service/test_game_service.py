import random
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from src.dto.game_state import GameState
from src.model.card import Card, CardSuit, CardValue
from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack
from src.repository.game_state_repository import GameStateRepository

# from src.repository.player_repository import PlayerRepository
from src.service.game_service import GameService

# from src.model.stack import WonStack


def compare(self, other):

    if not type(self) == type(other):
        return False

    if self.game != other.game:
        return False

    if self.player_stacks != other.player_stacks:
        return False

    if self.player_hands != other.player_hands:
        return False

    return True


class Matcher:
    def __init__(self, compare_func, obj):
        self.compare_func = compare_func
        self.obj = obj

    def __eq__(self, other):
        return self.compare_func(self.obj, other)


class TestGameService(unittest.TestCase):
    def setUp(self):
        pass

    def test_bootstrap(self):
        # creating mocks
        mock_game_state_repository = MagicMock(spec=GameStateRepository)
        mock_datetime = MagicMock(spec=datetime)
        mock_datetime.utcnow.return_value = datetime(2020, 1, 1, 1, 1, 1)
        mock_random = MagicMock(spec=random)
        mock_random.randrange.return_value = 0
        game_id = "123"

        # injecting mocks
        game_service = GameService(game_state_repository=mock_game_state_repository)
        game_service.id_generator = MagicMock(return_value="123")
        game_service.datetime = mock_datetime
        game_service.random = mock_random

        # test
        game_service.bootstrap(game_id, Deck())

        expected_game_state = self.__get_game_state(game_id)
        # TODO: find proper names for Matcher&Co.
        match_foo = Matcher(compare, expected_game_state)
        mock_game_state_repository.save.assert_called_with(match_foo)

    def __get_game_state(self, game_id: str) -> GameState:
        now = datetime(2020, 1, 1, 1, 1, 1)

        # creating hands and deck
        hand1 = Hand()
        hand1.id = "123"
        hand1.game_id = game_id
        hand1.updated_at = now
        hand1.cards = [
            Card(CardValue.KING, CardSuit.CLUB),
            Card(CardValue.THREE, CardSuit.CLUB),
            Card(CardValue.ACE, CardSuit.CLUB),
        ]
        hand1.turn = 0

        hand2 = Hand()
        hand2.id = "123"
        hand2.game_id = game_id
        hand2.updated_at = now
        hand2.cards = [
            Card(CardValue.SEVEN, CardSuit.CLUB),
            Card(CardValue.JACK, CardSuit.CLUB),
            Card(CardValue.QUEEN, CardSuit.CLUB),
        ]
        hand2.turn = 1

        hands = [
            hand1,
            hand2,
        ]

        deck = Deck()
        deck.pick(6)

        game = Game()
        game.id = game_id
        game.cards = deck

        stack1 = Stack()
        stack1.id = "123"
        stack1.game_id = game_id

        stack2 = Stack()
        stack2.id = "123"
        stack2.game_id = game_id

        stacks = [stack1, stack2]

        game_state = GameState()

        game_state.game = game
        game_state.player_hands = hands
        game_state.player_stacks = stacks

        return game_state


# def test_game_service_create():

#     # creating expected values
#     now = datetime(2020, 1, 1, 1, 1, 1)
#     random_id = "abcdefgh"
#     expected_game = Game()
#     expected_game.id = random_id
#     expected_game.created_at = now

#     # creating expected hands
#     hand1 = Hand()
#     hand1.id = "123"
#     hand1.created_at = now
#     hand1.player_id = "1"
#     hand1.cards = [
#         Card(CardValue.ACE, CardSuit.HEART),
#         Card(CardValue.DEUCE, CardSuit.HEART),
#         Card(CardValue.THREE, CardSuit.HEART),
#     ]
#     hand1.turn = 0

#     hand2 = Hand()
#     hand2.id = "456"
#     hand2.created_at = now
#     hand2.player_id = "2"
#     hand2.cards = [
#         Card(CardValue.FOUR, CardSuit.HEART),
#         Card(CardValue.FIVE, CardSuit.HEART),
#         Card(CardValue.SIX, CardSuit.HEART),
#     ]
#     hand2.turn = 1

#     expected_hands = [
#         hand1,
#         hand2,
#     ]

#     expected_deck = Deck()

#     # creating expected won stacks
#     won_stack1 = WonStack()
#     won_stack1.id = "123"
#     won_stack1.player_id = "1"
#     won_stack1.cards = []

#     won_stack2 = WonStack()
#     won_stack2.id = "456"
#     won_stack2.player_id = "2"
#     won_stack2.cards = []

#     expected_won_stacks = [
#         won_stack1,
#         won_stack2,
#     ]

#     # mocking repository
#     mock_game_repository = MagicMock(spec=GameRepository)
#     mock_game_repository.save.return_value = expected_player

#     # mocking datetime
#     mock_datetime = MagicMock(spec=datetime)
#     mock_datetime.now.return_value = now

#     # mocking id generator
#     mock_id_generator = MagicMock(return_value=random_id)

#     # injecting mocks into service
#     player_service = PlayerService(mock_player_repository)
#     player_service.datetime = mock_datetime
#     player_service.id_generator = mock_id_generator

#     # calling service
#     new_player = Player(id=None, name="johnny")
#     player = player_service.create(new_player)

#     assert player.id == random_id
#     assert player.name == "johnny"
#     assert player.created_at == now
#     assert player.last_seen == now
#     mock_player_repository.save.assert_called_with(new_player)
