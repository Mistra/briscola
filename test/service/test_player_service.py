

import unittest
from datetime import datetime
from typing import Tuple
from unittest.mock import MagicMock

from src.model.player import Player
from src.repository.player_repository import PlayerRepository
from src.service.player_service import PlayerService


class TestPlayerRepository(unittest.TestCase):
    def setUp(self):
        # creating expected values
        now = datetime(2020, 1, 1, 1, 1, 1)
        random_id = "abcdefgh"
        self.expected_player = self.__expected_player(now, random_id)

        # get mocks
        (
            self.mock_player_repository,
            self.mock_datetime,
            self.mock_id_generator
        ) = self.__generate_mocks(now, random_id)

    def test_create(self):

        # injecting mocks into service
        player_service = PlayerService(self.mock_player_repository)
        player_service.datetime = self.mock_datetime
        player_service.id_generator = self.mock_id_generator

        # calling service
        new_player = Player()
        new_player.name = "johnny"
        player = player_service.create(new_player)

        self.assertEqual(player, self.expected_player)
        self.mock_player_repository.save.assert_called_with(new_player)

    def test_find_by_id(self):
        # injecting mocks into service
        player_service = PlayerService(self.mock_player_repository)
        player_service.datetime = self.mock_datetime
        player_service.id_generator = self.mock_id_generator

        player = player_service.find_by_id("abcdefgh")
        self.assertEqual(player, self.expected_player)
        self.mock_player_repository.find_by_id.assert_called_with("abcdefgh")

    def test_delete_by_id(self):
        # injecting mocks into service
        player_service = PlayerService(self.mock_player_repository)
        player_service.datetime = self.mock_datetime
        player_service.id_generator = self.mock_id_generator

        player_service.delete_by_id("abcdefgh")
        self.mock_player_repository.delete_by_id.assert_called_with("abcdefgh")

    def __generate_mocks(self, now, random_id) -> Tuple[PlayerRepository, datetime, any]:
        expected_player = self.__expected_player(now, random_id)

        # mocking repository
        mock_player_repository = MagicMock(spec=PlayerRepository)
        mock_player_repository.save.return_value = expected_player
        mock_player_repository.find_by_id.return_value = expected_player
        mock_player_repository.delete_by_id.return_value = None

        # mocking datetime
        mock_datetime = MagicMock(spec=datetime)
        mock_datetime.now.return_value = now

        # mocking id generator
        mock_id_generator = MagicMock(return_value=random_id)

        return (
            mock_player_repository,
            datetime,
            mock_id_generator
        )

    def __expected_player(self, now, random_id) -> Player:

        player = Player()
        player.id = random_id
        player.name = "johnny"
        player.created_at = now

        return player
