

from src.model.lobby_player import LobbyPlayer
from src.repository.db_factory import get_db_connection


class LobbyPlayerRepository():
    def __init__(self):
        self.database = get_db_connection()

    def save(self, lobby_player):
        cursor = self.database.cursor()
        cursor.execute(
            "INSERT INTO lobby_player (id, lobby_id, player_id) VALUES (?, ?, ?)",
            (lobby_player.id, lobby_player.lobby_id, lobby_player.player_id))
        self.database.commit()
        return lobby_player

    def get_by_lobby_id(self, lobby_id):
        cursor = self.database.cursor()
        cursor.execute(
            "SELECT * FROM lobby_player WHERE lobby_id = ?", (lobby_id,))
        rows = cursor.fetchall()
        return [LobbyPlayer(row[0], row[1], row[2]) for row in rows]
