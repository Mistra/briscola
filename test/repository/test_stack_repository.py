

import re
import sqlite3
import unittest

import jsonpickle
from src.model.card import Card, CardSuit, CardValue
from src.model.stack import Stack
from src.repository.stack_repository import StackRepository


class TestStackRepository(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect(":memory:")
        cursor = self.db_conn.cursor()

        create_table_sql = None

        # reading directly from schema definition
        with (open("database/schema.sql", mode="r", encoding="utf-8")) as file:
            schema = file.read()
            regexp = "CREATE.*stack\\s[^;]*;"
            create_table_sql = re.search(regexp, schema).group()

        cursor.execute(create_table_sql)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        stack = self.__dummy_stack()
        stack_repository = StackRepository(self.db_conn)
        stack_repository.save(stack)

        query = "SELECT * FROM stack"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[0], stack.id)
        self.assertEqual(row[1], stack.game_id)
        self.assertEqual(row[2], stack.player_id)
        self.assertEqual(row[3], jsonpickle.encode(stack.cards))

    def test_update(self):
        stack = self.__dummy_stack()
        stack_repository = StackRepository(self.db_conn)
        stack_repository.save(stack)

        stack.player_id = "678"
        stack_repository.save(stack)

        query = "SELECT * FROM stack"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[2], "678")

    def test_find_by_id(self):
        stack_repository = StackRepository(self.db_conn)
        stack = self.__dummy_stack()

        result = stack_repository.find_by_id(stack.id)
        self.assertEqual(result, None)

        stack_repository.save(stack)
        result = stack_repository.find_by_id(stack.id)
        self.assertEqual(result, stack)

    def test_delete_by_id(self):
        stack_repository = StackRepository(self.db_conn)
        stack = self.__dummy_stack()
        stack_repository.save(stack)
        stack_repository.delete_by_id(stack.id)

        result = stack_repository.find_by_id(stack.id)
        self.assertEqual(result, None)

    def __dummy_stack(self) -> Stack:

        cards = [
            Card(CardValue.ACE, CardSuit.HEART),
            Card(CardValue.DEUCE, CardSuit.HEART)
        ]

        stack = Stack()
        stack.id = "123"
        stack.game_id = "234"
        stack.player_id = "345"
        stack.cards = cards

        return stack


if __name__ == '__main__':
    unittest.main()
