import logging
from contextlib import closing

from src.dto.game_state import GameState
from src.model.game import Game
from src.repository.db_factory import get_db_connection
from src.repository.game_player_repository import GamePlayerRepository
from src.repository.game_repository import GameRepository
from src.repository.hand_repository import HandRepository
from src.repository.stack_repository import StackRepository


class GameStateRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def save(self, game_state: GameState) -> GameState:
        logging.debug("Saving game_state for game with id %s", game_state.game.id)

        number_of_players = game_state.get_number_of_players()

        with closing(self.connection.cursor()) as cursor:
            game = self.__update_saved_game(game_state.game, cursor)
            player_ids = self.__fetch_player_ids(game.id, number_of_players, cursor)
            for idx, hand in enumerate(game_state.player_hands):
                # FIXME: prolly here it's best to bind hands and stacks to game_player!!!
                hand.player_id = player_ids[idx]
                HandRepository.raw_insert_or_replace(hand, cursor)
            for idx, stack in enumerate(game_state.player_stacks):
                stack.player_id = player_ids[idx]
                StackRepository.raw_insert_or_replace(stack, cursor)
            self.connection.commit()

        return game_state

    def __update_saved_game(self, current_game: Game, cursor) -> Game:
        saved_game = GameRepository.raw_find_by_id(current_game.id, cursor)
        if saved_game is None:
            raise Exception(f"Game ${current_game.id} doesn't exist, can't bootstrap.")
        saved_game.deck = current_game.deck
        GameRepository.raw_insert_or_replace(saved_game, cursor)
        return saved_game

    def __fetch_player_ids(
        self, game_id: str, number_of_players: int, cursor
    ) -> list[str]:
        game_players = GamePlayerRepository.raw__find_by_game_id(game_id, cursor)
        if len(game_players) != number_of_players:
            raise Exception(f"Game ${game_id} doesn't have a proper number of players.")
        return list(map(lambda game_player: game_player.player_id, game_players))
