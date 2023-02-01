import re
import sqlite3
import unittest
from datetime import datetime

import jsonpickle

from src.model.deck import Deck
from src.model.game import Game
from src.repository.game_repository import GameRepository


class TestGameRepository(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = self.db_conn.cursor()

        create_table_sql = None

        # reading directly from schema definition
        with (open("database/schema.sql", mode="r", encoding="utf-8")) as file:
            schema = file.read()
            regexp = "CREATE.*game\\s[^;]*;"
            create_table_sql = re.search(regexp, schema).group()

        cursor.execute(create_table_sql)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        game = self.__dummy_game()
        game_repository = GameRepository(self.db_conn)
        game_repository.save(game)

        query = "SELECT * FROM game"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[0], game.id)
        self.assertEqual(row[1], datetime(2000, 1, 1, 0, 0, 0))
        self.assertEqual(row[2], jsonpickle.encode(game.cards))

    def test_update(self):
        game = self.__dummy_game()
        game_repository = GameRepository(self.db_conn)
        game_repository.save(game)

        game.created_at = datetime(2000, 1, 2, 0, 0, 0)
        game_repository.save(game)

        query = "SELECT * FROM game"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[1], datetime(2000, 1, 2, 0, 0, 0))

    def test_find_by_id(self):
        game_repository = GameRepository(self.db_conn)
        game = self.__dummy_game()

        result = game_repository.find_by_id(game.id)
        self.assertEqual(result, None)

        game_repository.save(game)
        result = game_repository.find_by_id(game.id)
        self.assertEqual(result, game)

    def test_delete_by_id(self):
        game_repository = GameRepository(self.db_conn)
        game = self.__dummy_game()
        game_repository.save(game)
        game_repository.delete_by_id(game.id)

        result = game_repository.find_by_id(game.id)
        self.assertEqual(result, None)

    def __dummy_game(self) -> Game:
        game = Game()
        game.id = "123-456"
        game.created_at = datetime(2000, 1, 1, 0, 0, 0)
        game.cards = Deck()
        return game


if __name__ == "__main__":
    unittest.main()
