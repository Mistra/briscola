

import logging
from datetime import datetime

from src.model.game_player import GamePlayer
from src.repository.db_factory import get_db_connection


class GamePlayerRepository:
    database = None

    def __init__(self, db_conn=None):
        self.database = db_conn if db_conn is not None else get_db_connection()

    def save(self, game_player):
        logging.debug("Saving game_player with id %s", game_player.id)

        query = '''
        INSERT OR REPLACE INTO game_player (
            id,
            game_id,
            player_id
        ) VALUES (?, ?, ?)
        '''

        self.database.execute(
            query,
            (
                game_player.id,
                game_player.game_id,
                game_player.player_id
            )
        )
        self.database.commit()
        return game_player

    def find_by_id(self, game_player_id):
        logging.debug(
            "Attempting to fetch game_player with id %s", game_player_id)

        query = "SELECT * FROM game_player WHERE id = ?"
        row = self.database.execute(query, (game_player_id,)).fetchone()

        if row is not None:
            return self.__row_to_game_player(row)

        return None

    def delete_by_id(self, game_player_id):
        logging.debug(
            "Attempting to delete game_player with id %s", game_player_id)

        query = "DELETE FROM game_player WHERE id = ?"
        self.database.execute(query, (game_player_id,))
        self.database.commit()

    def __row_to_game_player(self, row):
        game_player = GamePlayer()
        game_player.id = row[0]
        game_player.game_id = row[1]
        game_player.player_id = row[2]
        return game_player
