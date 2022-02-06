
import logging

from src.model.player import Player
from src.repository.db_factory import get_db_connection


class PlayerRepository:
    database = None

    def __init__(self):
        self.database = get_db_connection()

    def save(self, player):
        logging.debug("Saving player to the database %s", player.__dict__)
        self.database.execute(
            "INSERT INTO player (id, name, created_at, last_seen) VALUES (?, ?, ?, ?)",
            (player.id, player.name, player.created_at, player.last_seen)
        )
        self.database.commit()
        return player

    def get_by_id(self, player_id):
        logging.debug(
            "Fetching player with id %s from the database", player_id)
        row = self.database.execute(
            "SELECT * FROM player WHERE id = ?", (player_id,)).fetchone()
        if row is not None:
            return Player(row[0], row[1], row[2], row[3])
        return None

    def get_all(self):
        logging.debug("Fetching all players from the database")
        rows = self.database.execute("SELECT * FROM player").fetchall()
        # convert rows to Player objects
        return [Player(row[0], row[1], row[2], row[3]) for row in rows]

    def delete_by_id(self, player_id):
        logging.debug(
            "Deleting player with id %s from the database", player_id)
        self.database.execute(
            "DELETE FROM player WHERE id = ?", (player_id,))
        self.database.commit()
