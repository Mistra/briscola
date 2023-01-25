

import logging
from datetime import datetime
from uuid import uuid4 as uuid

from src.repository.player_repository import PlayerRepository


class PlayerService():
    player_repository = None
    datetime = None
    id_generator = None

    def __init__(self, player_repo=None):
        self.player_repository = player_repo or PlayerRepository()
        self.datetime = datetime
        self.id_generator = uuid

    def create(self, player):
        player.id = str(self.id_generator())
        player.created_at = self.datetime.utcnow()
        logging.info("Creating player: %s", player.__dict__)
        player = self.player_repository.save(player)
        return player

    def find_by_id(self, player_id):
        return self.player_repository.find_by_id(player_id)

    def delete_by_id(self, player_id):
        self.player_repository.delete_by_id(player_id)
