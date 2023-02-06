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
    def __init__(
        self,
        db_conn=None,
        move_is_valid=lambda current_game_state, new_game_state: bool,
        update_game_state=lambda current_game_state, new_game_state: GameState,
    ):
        self.connection = db_conn if db_conn is not None else get_db_connection()
        self.move_is_valid = move_is_valid
        self.update_game_state = update_game_state

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

    def update(self, partial_game_state: GameState) -> GameState:
        logging.debug(
            "Updating game_state for game with id %s with state %s",
            partial_game_state.game.id,
            partial_game_state,
        )

        with closing(self.connection.cursor()) as cursor:
            current_game_state = self.__extract_game_state(partial_game_state, cursor)

            if not self.move_is_valid(current_game_state, partial_game_state):
                raise InvalidMoveException("Invalid move, received. Raising exception")

            game_state = self.update_game_state(current_game_state, partial_game_state)
            self.__update_saved_game(game_state.game, cursor)
            for hand in game_state.player_hands:
                HandRepository.raw_insert_or_replace(hand, cursor)
            for stack in game_state.player_stacks:
                StackRepository.raw_insert_or_replace(stack, cursor)
            self.connection.commit()
            return game_state

    def __extract_game_state(self, game_id: str, cursor) -> GameState:
        query = """
            SELECT g.*, h.*, s.* from game g
            JOIN hand h
            ON h.game_id = g.id
            JOIN stack s
            ON g.game_id = g.id
            WHERE game.id = ?
        """
        rows = cursor.execute(query, (game_id,)).fetchall()
        return self.__rows_to_game_state(rows)

    @staticmethod
    def __rows_to_game_state(rows) -> GameState:
        hand_rows = []
        stack_rows = []
        for idx, row in enumerate(rows):
            game_row = row[0:3] if idx == 0 else game_row  # game is repeated
            hand_rows.append(row[3:10])
            stack_rows.append(row[10:14])

        game = GameRepository.__row_to_game(game_row)
        hands = [HandRepository.__row_to_hand(hand_row) for hand_row in hand_rows]
        stack = [StackRepository.__row_to_stack(stack_row) for stack_row in stack_rows]

        game_state = GameState()
        game_state.game = game
        game_state.player_hands = hands
        game_state.player_stacks = stack

        return game_state

    def __update_saved_game(self, current_game: Game, cursor) -> Game:
        saved_game = GameRepository.raw_find_by_id(current_game.id, cursor)
        if saved_game is None:
            raise Exception(f"Game {current_game.id} doesn't exist, can't bootstrap.")
        saved_game.deck = current_game.deck
        GameRepository.raw_insert_or_replace(saved_game, cursor)
        return saved_game

    def __fetch_player_ids(
        self, game_id: str, number_of_players: int, cursor
    ) -> list[str]:
        game_players = GamePlayerRepository.raw__find_by_game_id(game_id, cursor)
        if len(game_players) != number_of_players:
            raise Exception(f"Game {game_id} doesn't have a proper number of players.")
        return list(map(lambda game_player: game_player.player_id, game_players))


class InvalidMoveException(Exception):
    pass
