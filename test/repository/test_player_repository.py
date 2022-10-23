

import re
import sqlite3
import unittest
from datetime import datetime

from src.model.player import Player
from src.repository.player_repository import PlayerRepository


class TestPlayerRepository(unittest.TestCase):
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
            regexp = "CREATE.*\\splayer\\s[^;]*;"
            create_table_sql = re.search(regexp, schema).group()

        cursor.execute(create_table_sql)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        player = self.__dummy_player()
        player_repository = PlayerRepository(self.db_conn)
        player_repository.save(player)

        query = "SELECT * FROM player"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[0], player.id)
        self.assertEqual(row[1], player.name)
        self.assertEqual(row[2], datetime(2000, 1, 1, 0, 0, 0))

    def test_update(self):
        player = self.__dummy_player()
        player_repository = PlayerRepository(self.db_conn)
        player_repository.save(player)

        player.name = "jim"
        player_repository.save(player)

        query = "SELECT * FROM player"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[1], "jim")

    def test_find_by_id(self):
        player_repository = PlayerRepository(self.db_conn)
        player = self.__dummy_player()

        result = player_repository.find_by_id(player.id)
        self.assertEqual(result, None)

        player_repository.save(player)
        result = player_repository.find_by_id(player.id)
        self.assertEqual(result, player)

    def test_delete_by_id(self):
        player_repository = PlayerRepository(self.db_conn)
        player = self.__dummy_player()
        player_repository.save(player)
        player_repository.delete_by_id(player.id)

        result = player_repository.find_by_id(player.id)
        self.assertEqual(result, None)

    def __dummy_player(self) -> Player:
        player = Player()
        player.id = "123"
        player.name = "nick"
        player.created_at = datetime(2000, 1, 1, 0, 0, 0)

        return player


if __name__ == '__main__':
    unittest.main()
