
import logging

from src.repository.db_factory import get_db_connection


class GameRepository:
    database = None

    def __init__(self):
        self.database = get_db_connection()

    def save(self, game):
        logging.debug("Saving game to the database %s", game.__dict__)

        # implement me...

        return game
