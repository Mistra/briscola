import logging
from contextlib import closing
from typing import Optional

import jsonpickle

from src.model.game import Game
from src.repository.db_factory import get_db_connection


class GameRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def save(self, game):
        logging.debug("Saving game with id %s", game.id)

        with closing(self.connection.cursor()) as cursor:
            self.raw_insert_or_replace(game, cursor)
            self.connection.commit()

        return game

    def find_by_id(self, game_id: str) -> Optional[Game]:
        logging.debug("Attempting to fetch game with id %s", game_id)
        with closing(self.connection.cursor()) as cursor:
            return self.raw_find_by_id(game_id, cursor)

    def delete_by_id(self, game_id: str) -> None:
        logging.debug("Attempting to delete game with id %s", game_id)
        query = "DELETE FROM game WHERE id = ?"
        self.connection.execute(query, (game_id,))

    @staticmethod
    def __row_to_game(row):
        game = Game()
        game.id = row[0]
        game.created_at = row[1]
        game.cards = jsonpickle.decode(row[2])
        return game

    @staticmethod
    def raw_find_by_id(game_id: str, cursor) -> Optional[Game]:
        query = "SELECT * FROM game WHERE id = ?"

        row = cursor.execute(query, (game_id,)).fetchone()
        if row is not None:
            return GameRepository.__row_to_game(row)
        return None

    @staticmethod
    def raw_insert_or_replace(game: Game, cursor):
        query = """
        INSERT OR REPLACE INTO game (
            id,
            created_at,
            cards
        ) VALUES (?, ?, ?)
        """

        cursor.execute(query, (game.id, game.created_at, jsonpickle.encode(game.cards)))


class UndefinedGameException(Exception):
    pass


class FullGameException(Exception):
    pass
