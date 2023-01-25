

import logging

from src.model.game_player import GamePlayer
from src.repository.db_factory import get_db_connection
from src.repository.transaction import transactional


class GamePlayerRepository:
    connection = None

    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    @transactional
    def save(self, game_player, cursor=None):
        logging.debug("Saving game_player with id %s", game_player.id)

        # cursor = self.connection.cursor()
        query = '''
        INSERT OR REPLACE INTO game_player (
            id,
            game_id,
            player_id
        ) VALUES (?, ?, ?)
        '''

        cursor.execute(
            query,
            (
                game_player.id,
                game_player.game_id,
                game_player.player_id
            )
        )
        # self.connection.commit()
        # cursor.close()
        return game_player

    def find_by_id(self, game_player_id):
        logging.debug("Fetching game_player with id %s", game_player_id)

        cursor = self.connection.cursor()
        query = "SELECT * FROM game_player WHERE id = ?"
        row = cursor.execute(query, (game_player_id,)).fetchone()

        if row is not None:
            return self.__row_to_game_player(row)

        return None

    def delete_by_id(self, game_player_id):
        logging.debug("Deleting game_player with id %s", game_player_id)

        cursor = self.connection.cursor()
        query = "DELETE FROM game_player WHERE id = ?"
        cursor.execute(query, (game_player_id,))
        self.connection.commit()

    def __row_to_game_player(self, row):
        game_player = GamePlayer()
        game_player.id = row[0]
        game_player.game_id = row[1]
        game_player.player_id = row[2]
        return game_player
