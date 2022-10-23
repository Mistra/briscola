

import unittest
from datetime import datetime
from typing import Tuple
from unittest.mock import MagicMock

from src.model.player import Player
from src.repository.player_repository import PlayerRepository
from src.service.player_service import PlayerService


class TestPlayerRepository(unittest.TestCase):
    def test_player_service_create(self):

        # creating expected values
        now = datetime(2020, 1, 1, 1, 1, 1)
        random_id = "abcdefgh"
        expected_player = self.__expected_player(now, random_id)

        # get mocks
        (
            mock_player_repository,
            mock_datetime,
            mock_id_generator
        ) = self.__generate_mocks(now, random_id)

        # injecting mocks into service
        player_service = PlayerService(mock_player_repository)
        player_service.datetime = mock_datetime
        player_service.id_generator = mock_id_generator

        # calling service
        new_player = Player()
        new_player.name = "johnny"
        player = player_service.create(new_player)

        self.assertEqual(player, expected_player)

        mock_player_repository.save.assert_called_with(new_player)

    def __generate_mocks(self, now, random_id) -> Tuple[PlayerRepository, datetime, any]:
        expected_player = self.__expected_player(now, random_id)

        # mocking repository
        mock_player_repository = MagicMock(spec=PlayerRepository)
        mock_player_repository.save.return_value = expected_player

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
