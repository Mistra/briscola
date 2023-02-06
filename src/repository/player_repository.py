import logging
from contextlib import closing
from typing import Optional

from src.model.player import Player
from src.repository.db_factory import get_db_connection


class PlayerRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def save(self, player):
        logging.debug("Saving player with id %s", player.id)

        query = """
        INSERT OR REPLACE INTO player (
            id,
            name,
            created_at
        ) VALUES (?, ?, ?)
        """

        self.connection.execute(query, (player.id, player.name, player.created_at))
        self.connection.commit()
        return player

    def find_by_id(self, player_id):
        logging.debug("Attempting to fetch player with id %s", player_id)

        with closing(self.connection.cursor()) as cursor:
            return self.raw_find_by_id(player_id, cursor)

    @staticmethod
    def raw_find_by_id(player_id: str, cursor) -> Optional[Player]:
        query = "SELECT * FROM player WHERE id = ?"
        row = cursor.execute(query, (player_id,)).fetchone()

        if row is not None:
            return PlayerRepository.__row_to_player(row)

        return None

    def delete_by_id(self, player_id):
        logging.debug("Attempting to delete player with id %s", player_id)

        query = "DELETE FROM player WHERE id = ?"
        self.connection.execute(query, (player_id,))
        self.connection.commit()

    @staticmethod
    def __row_to_player(row):
        player = Player()
        player.id = row[0]
        player.name = row[1]
        player.created_at = row[2]
        return player


class UndefinedPlayerException(Exception):
    pass
