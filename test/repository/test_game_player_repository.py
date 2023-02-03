import sqlite3
import unittest
from datetime import datetime

from src.model.game import Game
from src.model.game_player import GamePlayer
from src.model.player import Player
from src.repository.game_player_repository import GamePlayerRepository
from src.repository.game_repository import (
    FullGameException,
    GameRepository,
    UndefinedGameException,
)
from src.repository.player_repository import PlayerRepository, UndefinedPlayerException


class TestGamePlayerRepository(unittest.TestCase):
    def setUp(self):
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
        number_of_players = 2
        game_player = GamePlayer("gp1", "g1", "p1")
        game_player_repository = GamePlayerRepository(self.db_conn)
        player_repository = PlayerRepository(self.db_conn)
        game_repository = GameRepository(self.db_conn)

        # checks for UndefinedPlayerException if player is not present
        with self.assertRaises(UndefinedPlayerException):
            game_player_repository.create(game_player, number_of_players)

        # create player
        player = Player("p1", "timmy", datetime(2000, 1, 1, 0, 0, 0))
        player_repository.save(player)

        # checks for UndefinedGameException if game is not present
        with self.assertRaises(UndefinedGameException):
            game_player_repository.create(game_player, number_of_players)

        # create game
        game_repository.save(Game("g1", datetime(2000, 1, 1, 0, 0, 0)))

        # checks the game is created flawlessly
        result_game_player = game_player_repository.create(
            game_player, number_of_players
        )
        self.assertEqual(result_game_player, game_player)

        # create 2 other players and game_players
        player2 = Player("p2", "jimmy", datetime(2000, 1, 1, 0, 0, 0))
        player3 = Player("p3", "johnny", datetime(2000, 1, 1, 0, 0, 0))
        player_repository.save(player2)
        player_repository.save(player3)
        game_player2 = GamePlayer("gp2", "g1", "p2")
        game_player3 = GamePlayer("gp3", "g1", "p3")

        # insert second game_player
        game_player_repository.create(game_player2, number_of_players)

        # checks for FullGameException if game is full
        with self.assertRaises(FullGameException):
            game_player_repository.create(game_player3, number_of_players)

    def test_update(self):
        game_player = GamePlayer("gp1", "g1", "p1")
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player_repository.save(game_player)

        game_player.game_id = "g2"
        game_player_repository.save(game_player)

        query = "SELECT * FROM game_player"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[1], "g2")

    def test_find_by_id(self):
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player = GamePlayer("gp1", "g1", "p1")

        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, None)

        game_player_repository.save(game_player)
        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, game_player)

    def test_delete_by_id(self):
        game_player_repository = GamePlayerRepository(self.db_conn)
        game_player = GamePlayer("gp1", "g1", "p1")
        game_player_repository.save(game_player)
        game_player_repository.delete_by_id(game_player.id)

        result = game_player_repository.find_by_id(game_player.id)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
