

from datetime import datetime
from unittest.mock import MagicMock

from src.model.player import Player
from src.repository.player_repository import PlayerRepository
from src.service.player_service import PlayerService


def test_player_service_create():

    # creating expected values
    now = datetime(2020, 1, 1, 1, 1, 1)
    random_id = "abcdefgh"
    expected_player = Player(id=random_id, name="johnny",
                             created_at=now, last_seen=now)

    # mocking repository
    mock_player_repository = MagicMock(spec=PlayerRepository)
    mock_player_repository.save.return_value = expected_player

    # mocking datetime
    mock_datetime = MagicMock(spec=datetime)
    mock_datetime.now.return_value = now

    # mocking id generator
    mock_id_generator = MagicMock(return_value=random_id)

    # injecting mocks into service
    player_service = PlayerService(mock_player_repository)
    player_service.datetime = mock_datetime
    player_service.id_generator = mock_id_generator

    # calling service
    new_player = Player(id=None, name="johnny")
    player = player_service.create(new_player)

    assert player.id == random_id
    assert player.name == "johnny"
    assert player.created_at == now
    assert player.last_seen == now
    mock_player_repository.save.assert_called_with(new_player)
