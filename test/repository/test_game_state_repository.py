import sqlite3
import unittest
from datetime import datetime

from flask import Flask

from src.dto.game_state import GameState
from src.model.card import Card, CardSuit, CardValue
from src.model.deck import Deck
from src.model.game import Game
from src.model.hand import Hand
from src.model.stack import Stack
from src.repository.game_state_repository import GameStateRepository


class TestGameStateRepository(unittest.TestCase):
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
        game_state = self.__dummy_game_state()
        game_state_repository = GameStateRepository(self.db_conn)
        game_state_repository.save(game_state)

        query = "SELECT * FROM game"
        row = self.db_conn.execute(query).fetchone()
        self.assertEqual(row[1], datetime(2000, 1, 1, 0, 0, 0))

        query = "SELECT * FROM stack"
        row = self.db_conn.execute(query).fetchall()
        self.assertEqual(2, len(row))

        query = "SELECT * FROM player_hand"
        row = self.db_conn.execute(query).fetchall()
        self.assertEqual(2, len(row))

    def __dummy_game_state(self) -> GameState:
        hand1 = self.__dummy_hand()
        hand1.id = "123-234"
        hand1.player_id = "123-123"

        hand2 = self.__dummy_hand()
        hand2.id = "123-345"
        hand2.player_id = "123-321"

        stack1 = self.__dummy_stack()
        stack1.id = "234-234"
        stack1.player_id = "123-123"

        stack2 = self.__dummy_stack()
        stack2.id = "234-345"
        stack2.player_id = "123-321"

        game = self.__dummy_game()

        game_state = GameState()
        game_state.player_hands = [hand1, hand2]
        game_state.player_stacks = [stack1, stack2]
        game_state.game = game

        return game_state

    def __dummy_game(self) -> Game:
        game = Game()
        game.id = "456-456"
        game.created_at = datetime(2000, 1, 1, 0, 0, 0)
        game.cards = Deck()
        return game

    def __dummy_hand(self) -> Hand:
        cards = [
            Card(CardValue.ACE, CardSuit.HEART),
            Card(CardValue.DEUCE, CardSuit.HEART),
            Card(CardValue.THREE, CardSuit.HEART),
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

    def __dummy_stack(self) -> Stack:

        cards = [
            Card(CardValue.ACE, CardSuit.HEART),
            Card(CardValue.DEUCE, CardSuit.HEART),
        ]

        stack = Stack()
        stack.id = "123"
        stack.game_id = "456-456"
        stack.player_id = "1"
        stack.cards = cards

        return stack


if __name__ == "__main__":
    unittest.main()
