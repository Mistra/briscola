'''Sqlite Lobby Repository module'''


import logging

from src.model.lobby import Lobby
from src.repository.db_factory import get_db_connection


class LobbyRepository:
    database = None

    def __init__(self):
        self.database = get_db_connection()

    def save(self, lobby):
        logging.debug("Saving lobby to the database %s", lobby.__dict__)
        self.database.execute(
            "INSERT INTO lobby (id, created_at, last_activity_at) VALUES (?, ?, ?)",
            (lobby.id, lobby.created_at, lobby.last_activity_at)
        )
        self.database.commit()
        return lobby

    def get_by_id(self, lobby_id):
        logging.debug("Fetching lobby with id %s from the database", lobby_id)
        row = self.database.execute(
            "SELECT * FROM lobby WHERE id = ?", (lobby_id,)).fetchone()
        if row is not None:
            return Lobby(row[0], row[1], row[2])
        return None

    def get_all(self):
        logging.debug("Fetching all lobbies from the database")
        rows = self.database.execute("SELECT * FROM lobby").fetchall()
        # convert rows to Lobby objects
        return [Lobby(row[0], row[1], row[2]) for row in rows]

    def delete_by_id(self, lobby_id):
        logging.debug(
            "Deleting lobby with id %s from the database", lobby_id)
        self.database.execute(
            "DELETE FROM lobby WHERE id = ?", (lobby_id,))
        self.database.commit()
