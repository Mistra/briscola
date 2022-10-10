

from datetime import datetime
from unittest.mock import MagicMock

from src.model.card import Card, CardSuit, CardValue
from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.won_stack import WonStack
from src.repository.game_repository import GameRepository
# from src.repository.player_repository import PlayerRepository
from src.service.game_service import GameService

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
