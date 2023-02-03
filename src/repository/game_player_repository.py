import logging
from contextlib import closing
from typing import Optional

from src.model.game_player import GamePlayer
from src.repository.db_factory import get_db_connection
from src.repository.game_repository import (
    FullGameException,
    GameRepository,
    UndefinedGameException,
)
from src.repository.player_repository import PlayerRepository, UndefinedPlayerException


class GamePlayerRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def create(self, game_player: GamePlayer, number_of_players: int) -> GamePlayer:
        logging.debug("Creating game_player with id %s", game_player.id)

        with closing(self.connection.cursor()) as cursor:
            self.__check_player_exists(game_player.player_id, cursor)
            self.__check_game_exists(game_player.game_id, cursor)
            self.__check_game_is_joinable(game_player, number_of_players, cursor)

            self.raw__insert_or_replace(game_player, cursor)
            self.connection.commit()

        return game_player

    def save(self, game_player: GamePlayer):
        logging.debug("Saving game_player with id %s", game_player.id)

        with closing(self.connection.cursor()) as cursor:
            self.raw__insert_or_replace(game_player, cursor)
            self.connection.commit()

        return game_player

    def find_by_id(self, game_player_id) -> Optional[GamePlayer]:
        logging.debug("Fetching game_player with id %s", game_player_id)

        with closing(self.connection.cursor()) as cursor:
            query = "SELECT * FROM game_player WHERE id = ?"
            row = cursor.execute(query, (game_player_id,)).fetchone()

            if row is not None:
                return self.__row_to_game_player(row)

            return None

    def find_by_game_id(self, game_id) -> Optional[GamePlayer]:
        logging.debug("Fetching game_player with game_id %s", game_id)

        with closing(self.connection.cursor()) as cursor:
            query = "SELECT * FROM game_player WHERE game_id = ?"
            rows = cursor.execute(query, (game_id,)).fetchall()

            return [self.__row_to_game_player(row) for row in rows]

    def delete_by_id(self, game_player_id):
        logging.debug("Deleting game_player with id %s", game_player_id)

        with closing(self.connection.cursor()) as cursor:
            query = "DELETE FROM game_player WHERE id = ?"
            cursor.execute(query, (game_player_id,))
            self.connection.commit()

    @staticmethod
    def __row_to_game_player(row) -> Optional[GamePlayer]:
        game_player = GamePlayer()
        game_player.id = row[0]
        game_player.game_id = row[1]
        game_player.player_id = row[2]
        return game_player

    @staticmethod
    def raw__find_by_game_id(game_id: str, cursor) -> list[GamePlayer]:
        query = "SELECT * FROM game_player WHERE game_id = ?"
        rows = cursor.execute(query, (game_id,)).fetchall()

        return [GamePlayerRepository.__row_to_game_player(row) for row in rows]

    @staticmethod
    def raw__insert_or_replace(game_player: GamePlayer, cursor):
        query = """
        INSERT OR REPLACE INTO game_player (
            id,
            game_id,
            player_id
        ) VALUES (?, ?, ?)
        """

        cursor.execute(
            query, (game_player.id, game_player.game_id, game_player.player_id)
        )

    @staticmethod
    def __check_player_exists(player_id: str, cursor):
        existing_player = PlayerRepository.raw_find_by_id(player_id, cursor)
        if existing_player is None:
            raise UndefinedPlayerException(f"Player ${player_id} doesn't exist")

    @staticmethod
    def __check_game_is_joinable(
        game_player: GamePlayer, number_of_players: int, cursor
    ):
        game_id = game_player.game_id
        player_id = game_player.player_id

        existing_game_players = GamePlayerRepository.raw__find_by_game_id(
            game_id, cursor
        )
        if number_of_players <= len(existing_game_players):
            raise FullGameException(
                f"Player ${player_id} cannot join game ${game_id}, the game is full"
            )

    @staticmethod
    def __check_game_exists(game_id: str, cursor):
        existing_game = GameRepository.raw_find_by_id(game_id, cursor)
        if existing_game is None:
            raise UndefinedGameException(f"Game ${game_id} doesn't exist")
