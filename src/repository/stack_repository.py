import logging
from contextlib import closing

import jsonpickle

from src.model.stack import Stack
from src.repository.db_factory import get_db_connection


class StackRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def save(self, stack):
        logging.debug("Saving stack with id %s", stack.id)

        with closing(self.connection.cursor()) as cursor:
            self.raw_insert_or_replace(stack, cursor)
            self.connection.commit()

        return stack

    def find_by_id(self, stack_id: str) -> Stack | None:
        logging.debug("Attempting to fetch stack with id %s", stack_id)
        query = "SELECT * FROM stack WHERE id = ?"

        row = self.connection.execute(query, (stack_id,)).fetchone()
        if row is not None:
            return self.__row_to_stack(row)

        return None

    def delete_by_id(self, stack_id: str) -> None:
        logging.debug("Attempting to delete stack with id %s", stack_id)
        query = "DELETE FROM stack WHERE id = ?"
        self.connection.execute(query, (stack_id,))

    @staticmethod
    def __row_to_stack(row):
        stack = Stack()
        stack.id = row[0]
        stack.game_id = row[1]
        stack.player_id = row[2]
        stack.cards = jsonpickle.decode(row[3])
        return stack

    @staticmethod
    def raw_insert_or_replace(stack: Stack, cursor):
        query = """
        INSERT OR REPLACE INTO stack (
            id,
            game_id,
            player_id,
            cards
        ) VALUES (?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (stack.id, stack.game_id, stack.player_id, jsonpickle.encode(stack.cards)),
        )
