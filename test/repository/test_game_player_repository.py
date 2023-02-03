import re
import sqlite3
import unittest
from datetime import datetime

from flask import Flask

from src.model.game_player import GamePlayer
from src.model.player import Player
from src.repository.game_player_repository import GamePlayerRepository
from src.repository.player_repository import PlayerRepository, UndefinedPlayerException
from src.repository.game_repository import UndefinedGameException


class TestGamePlayerRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.db_conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = self.db_conn.cursor()

        # reading directly from schema definition
        with (open("database/schema.sql", mode="r", encoding="utf-8")) as file:
            schema = file.read()
            tables = schema.split(";")

        for table in tables:
            cursor.execute(table)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        # test __check_player_exists(game_player.player_id, cursor)
        # test __check_game_exists(game_player.game_id, cursor)
        # test __check_game_is_joinable(game_player, number_of_players, cursor)
        number_of_players = 2

        game_player = self.__dummy_game_player()
        game_player_repository = GamePlayerRepository(self.db_conn)
        with self.assertRaises(UndefinedPlayerException):
            game_player_repository.create(game_player, number_of_players)
        player_repository = PlayerRepository(self.db_conn)
        player_repository.save(self.__dummy_player())
        with self.assertRaises(UndefinedGameException):
            game_player_repository.create(game_player, number_of_players)

    def test_update(self):
        with self.app.app_context():
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
        with self.app.app_context():
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

    def __dummy_player(self) -> Player:
        player = Player()
        player.id = "789"
        player.name = "shortcock"
        player.created_at = datetime(2000, 1, 1, 0, 0, 0)

        return player


if __name__ == "__main__":
    unittest.main()
