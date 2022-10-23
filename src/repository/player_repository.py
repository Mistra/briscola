

import logging
from datetime import datetime

from src.model.player import Player
from src.repository.db_factory import get_db_connection


class PlayerRepository:
    database = None

    def __init__(self, db_conn=None):
        self.database = db_conn if db_conn is not None else get_db_connection()

    def save(self, player):
        logging.debug("Saving player with id %s", player.id)

        query = '''
        INSERT OR REPLACE INTO player (
            id,
            name,
            created_at
        ) VALUES (?, ?, ?)
        '''

        self.database.execute(
            query,
            (
                player.id,
                player.name,
                player.created_at
            )
        )
        self.database.commit()
        return player

    def find_by_id(self, player_id):
        logging.debug("Attempting to fetch player with id %s", player_id)

        query = "SELECT * FROM player WHERE id = ?"
        row = self.database.execute(query, (player_id,)).fetchone()

        if row is not None:
            return self.__row_to_player(row)

        return None

    def delete_by_id(self, player_id):
        logging.debug("Attempting to delete player with id %s", player_id)

        query = "DELETE FROM player WHERE id = ?"
        self.database.execute(query, (player_id,))
        self.database.commit()

    def __row_to_player(self, row):
        player = Player()
        player.id = row[0]
        player.name = row[1]
        player.created_at = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        return player
