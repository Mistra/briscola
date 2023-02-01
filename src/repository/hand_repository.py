import logging
from contextlib import closing

import jsonpickle

from src.model.hand import Hand
from src.repository.db_factory import get_db_connection


class HandRepository:
    def __init__(self, db_conn=None):
        self.connection = db_conn if db_conn is not None else get_db_connection()

    def save(self, hand: Hand) -> Hand:
        logging.debug("Saving hand with id %s", hand.id)

        with closing(self.connection.cursor()) as cursor:
            self.raw_insert_or_replace(hand, cursor)
            self.connection.commit()

        return hand

    def find_by_id(self, hand_id: str) -> Hand:
        logging.debug("Attempting to fetch hand with id %s", hand_id)
        query = "SELECT * FROM player_hand WHERE id = ?"

        row = self.connection.execute(query, (hand_id,)).fetchone()
        if row is not None:
            return self.__row_to_hand(row)

        return None

    def find_by_game_id(self, game_id: str) -> list[Hand]:
        logging.debug("Attempting to fetch hand with game_id %s", game_id)
        query = "SELECT * FROM player_hand WHERE game_id = ?"

        rows = self.connection.execute(query, (game_id,)).fetchall()
        return [self.__row_to_hand(row) for row in rows]

    def delete_by_id(self, hand_id: str) -> None:
        logging.debug("Attempting to delete hand with id %s", hand_id)
        query = "DELETE FROM player_hand WHERE id = ?"
        self.connection.execute(query, (hand_id,))

    def __row_to_hand(self, row):
        hand = Hand()
        hand.id = row[0]
        hand.game_id = row[1]
        hand.player_id = row[2]
        hand.cards = jsonpickle.decode(row[3])
        hand.turn = row[4]
        hand.played_card = jsonpickle.decode(row[5])
        hand.updated_at = row[6]
        return hand

    @staticmethod
    def raw_insert_or_replace(hand: Hand, cursor):
        query = """
        INSERT OR REPLACE INTO player_hand (
            id,
            game_id,
            player_id,
            cards,
            turn,
            played_card,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                hand.id,
                hand.game_id,
                hand.player_id,
                jsonpickle.encode(hand.cards),
                hand.turn,
                jsonpickle.encode(hand.played_card),
                hand.updated_at,
            ),
        )
