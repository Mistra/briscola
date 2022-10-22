

import re
import sqlite3
import unittest
from datetime import datetime

import jsonpickle
from src.model.card import Card, CardSuit, CardValue
from src.model.hand import Hand
from src.repository.hand_repository import HandRepository


class TestHandRepository(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect(":memory:")
        cursor = self.db_conn.cursor()

        create_table_sql = None

        # reading directly from schema definition
        with (open("database/schema.sql", mode="r", encoding="utf-8")) as file:
            schema = file.read()
            regexp = "CREATE.*player_hand(.|\n)*;"
            create_table_sql = re.search(regexp, schema).group()

        cursor.execute(create_table_sql)
        self.db_conn.commit()

    def tearDown(self) -> None:
        self.db_conn.close()

    def test_create(self):
        hand = self.__dummy_hand()
        hand_repository = HandRepository(self.db_conn)
        hand_repository.save(hand)

        query = "SELECT * FROM player_hand"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[0], hand.id)
        self.assertEqual(row[1], hand.game_id)
        self.assertEqual(row[2], hand.player_id)
        self.assertEqual(row[3], jsonpickle.encode(hand.cards))
        self.assertEqual(row[4], hand.turn)
        self.assertEqual(row[5], jsonpickle.encode(hand.played_card))
        self.assertEqual(row[6], "2000-01-01 00:00:00")

    def test_update(self):
        hand = self.__dummy_hand()
        hand_repository = HandRepository(self.db_conn)
        hand_repository.save(hand)

        hand.turn = 1
        hand_repository.save(hand)

        query = "SELECT * FROM player_hand"
        row = self.db_conn.execute(query).fetchone()

        self.assertEqual(row[4], 1)

    def test_find_by_id(self):
        hand_repository = HandRepository(self.db_conn)
        hand = self.__dummy_hand()

        result = hand_repository.find_by_id(hand.id)
        self.assertEqual(result, None)

        hand_repository.save(hand)
        result = hand_repository.find_by_id(hand.id)
        self.assertEqual(result, hand)

    def test_find_by_game_id(self):
        hand_repository = HandRepository(self.db_conn)
        hand1 = self.__dummy_hand()
        hand2 = self.__dummy_hand()
        hand2.id = "123-457"

        result = hand_repository.find_by_game_id(hand1.game_id)
        self.assertEqual(result, [])

        hand_repository.save(hand1)
        hand_repository.save(hand2)

        result = hand_repository.find_by_game_id(hand1.game_id)
        self.assertEqual(result, [hand1, hand2])

    def test_delete_by_id(self):
        hand_repository = HandRepository(self.db_conn)
        hand = self.__dummy_hand()
        hand_repository.save(hand)
        hand_repository.delete_by_id(hand.id)

        result = hand_repository.find_by_id(hand.id)
        self.assertEqual(result, None)

    def __dummy_hand(self) -> Hand:
        cards = [
            Card(CardValue.ACE, CardSuit.HEART),
            Card(CardValue.DEUCE, CardSuit.HEART),
            Card(CardValue.THREE, CardSuit.HEART)
        ]

        hand = Hand()
        hand.id = "123-456"
        hand.game_id = "456-456"
        hand.player_id = "123-123"
        hand.cards = cards
        hand.turn = 0
        hand.played_card = Card(CardValue.ACE, CardSuit.HEART)
        hand.updated_at = datetime(2000, 1, 1, 0, 0, 0)
        return hand


if __name__ == '__main__':
    unittest.main()
