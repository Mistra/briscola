

import re
import sqlite3
import unittest

from src.model.game_player import GamePlayer
from src.repository.game_player_repository import GamePlayerRepository


class TestGamePlayerRepository(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect(
            ":memory:",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        cursor = self.db_conn.cursor()

        create_table_sql = None

        # reading directly from schema definition
        with (open("database/schema.sql", mode="r", encoding="utf-8")) as file:
            schema = file.read()
            regexp = "CREATE.*\\sgame_player\\s[^;]*;"
            create_table_sql = re.search(regexp, schema).group()

        cursor.execute(create_table_sql)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        game_player = self.__dummy_game_player()
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player_repository.save(game_player)

        query = "SELECT * FROM game_player"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[0], game_player.id)
        self.assertEqual(row[1], game_player.game_id)
        self.assertEqual(row[2], game_player.player_id)

    def test_update(self):
        game_player = self.__dummy_game_player()
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player_repository.save(game_player)

        game_player.game_id = "987"
        game_player_repository.save(game_player)

        query = "SELECT * FROM game_player"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[1], "987")

    def test_find_by_id(self):
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player = self.__dummy_game_player()

        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, None)

        game_player_repository.save(game_player)
        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, game_player)

    def test_delete_by_id(self):
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player = self.__dummy_game_player()
        game_player_repository.save(game_player)
        game_player_repository.delete_by_id(game_player.id)

        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, None)

    def __dummy_game_player(self) -> GamePlayer:
        game_player = GamePlayer()
        game_player.id = "123"
        game_player.game_id = "456"
        game_player.player_id = "789"

        return game_player


if __name__ == '__main__':
    unittest.main()
