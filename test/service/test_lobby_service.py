

from datetime import datetime
from unittest.mock import MagicMock

from src.model.lobby import Lobby
from src.model.lobby_player import LobbyPlayer
from src.repository.lobby_player_repository import LobbyPlayerRepository
from src.repository.lobby_repository import LobbyRepository
from src.service.lobby_service import LobbyService


def test_lobby_service_create():

    # creating expected values
    now = datetime(2020, 1, 1, 1, 1, 1)
    random_id = "abcdefghij"
    expected_lobby = Lobby(id=random_id, created_at=now, last_activity_at=now)

    # mocking repository
    mock_lobby_repository = MagicMock(spec=LobbyRepository)
    mock_lobby_player_repository = MagicMock(spec=LobbyPlayerRepository)
    mock_lobby_repository.save.return_value = expected_lobby

    # mocking datetime
    mock_datetime = MagicMock(spec=datetime)
    mock_datetime.now.return_value = now

    # mocking id generator
    mock_id_generator = MagicMock(return_value=random_id)

    # injecting mocks into service
    lobby_service = LobbyService(
        mock_lobby_repository, mock_lobby_player_repository)
    lobby_service.datetime = mock_datetime
    lobby_service.id_generator = mock_id_generator

    # calling service
    empty_lobby = Lobby(id=None)
    lobby = lobby_service.create(empty_lobby)

    assert lobby.id == random_id
    assert lobby.created_at == now
    assert lobby.last_activity_at == now
    mock_lobby_repository.save.assert_called_with(empty_lobby)


def test_lobby_service_add_player():
    random_id = "abcdefghij"
    random_lobby_id = "klmnopqrst"
    random_player_id = "uvwxyz"
    expected_lobby_player = LobbyPlayer(
        id=random_id, lobby_id=random_lobby_id, player_id=random_player_id)

    mock_lobby_repository = MagicMock(spec=LobbyRepository)
    mock_lobby_player_repository = MagicMock(spec=LobbyPlayerRepository)
    mock_lobby_player_repository.save.return_value = expected_lobby_player
    lobby_service = LobbyService(
        mock_lobby_repository, mock_lobby_player_repository)
    lobby_service.id_generator = MagicMock(return_value=random_id)

    lobby_player = lobby_service.add_player(random_lobby_id, random_player_id)

    assert lobby_player.id == random_id
    assert lobby_player.lobby_id == random_lobby_id
    assert lobby_player.player_id == random_player_id
    mock_lobby_player_repository.save.assert_called()


def test_lobby_service_delete_by_id():
    random_id = "abcdefghij"

    mock_lobby_repository = MagicMock(spec=LobbyRepository)
    mock_lobby_player_repository = MagicMock(spec=LobbyPlayerRepository)
    lobby_service = LobbyService(
        mock_lobby_repository, mock_lobby_player_repository)

    lobby_service.delete_by_id(random_id)

    mock_lobby_repository.delete_by_id.assert_called_with(random_id)
