
import logging

import jsonpickle
from src.model.game import Game
from src.repository.db_factory import get_db_connection


class GameRepository:
    database = None

    def __init__(self, db_conn=None):
        self.database = db_conn if db_conn is not None else get_db_connection()

    def save(self, game):
        logging.debug("Saving game with id %s", game.id)

        query = '''
        INSERT OR REPLACE INTO game (
            id,
            created_at,
            cards
        ) VALUES (?, ?, ?)
        '''

        self.database.execute(
            query,
            (
                game.id,
                game.created_at,
                jsonpickle.encode(game.cards)
            )
        )
        self.database.commit()

        return game

    def find_by_id(self, game_id: str) -> Game | None:
        logging.debug("Attempting to fetch game with id %s", game_id)
        query = "SELECT * FROM game WHERE id = ?"

        row = self.database.execute(query, (game_id,)).fetchone()
        if row is not None:
            return self.__row_to_game(row)

        return None

    def delete_by_id(self, game_id: str) -> None:
        logging.debug("Attempting to delete game with id %s", game_id)
        query = "DELETE FROM game WHERE id = ?"
        self.database.execute(query, (game_id,))

    def __row_to_game(self, row):
        game = Game()
        game.id = row[0]
        game.created_at = row[1]
        game.cards = jsonpickle.decode(row[2])
        return game
