

import logging
from datetime import datetime
from uuid import uuid4 as uuid

from src.model.lobby_player import LobbyPlayer
from src.repository.lobby_player_repository import LobbyPlayerRepository
from src.repository.lobby_repository import LobbyRepository


class LobbyService:
    lobby_repository = None
    datetime = None
    id_generator = None

    def __init__(self, lobby_repo=None, lobby_player_repo=None):
        self.lobby_repository = lobby_repo or LobbyRepository()
        self.lobby_player_repository = lobby_player_repo or LobbyPlayerRepository()
        self.datetime = datetime
        self.id_generator = uuid

    def create(self, lobby):
        lobby.id = str(self.id_generator())
        lobby.created_at = self.datetime.now()
        lobby.last_activity_at = self.datetime.now()
        logging.info("Creating lobby: %s", lobby.__dict__)
        lobby = self.lobby_repository.save(lobby)
        return lobby

    def add_player(self, lobby_id, player_id):
        lobby_player = LobbyPlayer(
            str(self.id_generator()), lobby_id, player_id)
        logging.info("Adding player with id %s to lobby with id %s",
                     player_id, lobby_id)
        lobby_player = self.lobby_player_repository.save(lobby_player)
        return lobby_player

    def get_by_id(self, lobby_id):
        lobby = self.lobby_repository.get_by_id(lobby_id)
        for lobby_player in self.lobby_player_repository.get_by_lobby_id(lobby_id):
            lobby.add_player(lobby_player)
        return lobby

    def get_all(self):
        lobbies = self.lobby_repository.get_all()
        for lobby in lobbies:
            for lobby_player in self.lobby_player_repository.get_by_lobby_id(lobby.id):
                lobby.add_player(lobby_player.player_id)
        return lobbies

    def delete_by_id(self, lobby_id):
        self.lobby_repository.delete_by_id(lobby_id)
