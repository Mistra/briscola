# This is a simple in memory lobby repository

class LobbyRepository:
    lobbies = None

    def __init__(self):
        self.lobbies = {}

    def save(self, lobby):
        self.lobbies[lobby.id] = lobby
        return lobby

    def get_by_id(self, lobby_id):
        return self.lobbies[lobby_id]

    def get_all(self):
        return list(self.lobbies.values())

    def delete_by_id(self, lobby_id):
        del self.lobbies[lobby_id]
