
# I want a service with the following endpoints

# Create a lobby

import random
import string
from briscola.model.lobby import Lobby


def generate_10_chars_id():
    possible_id_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(possible_id_chars) for _ in range(10))


class LobbyService:
    def __init__(self, lobby_repository):
        self.lobby_repository = lobby_repository

    def create(self, lobby):
        lobby.id = generate_10_chars_id()
        self.lobby_repository.save(lobby)
        return lobby

    def get_by_id(self, lobby_id):
        return self.lobby_repository.get(lobby_id)

    def get_all(self):
        return self.lobby_repository.get_all()

    def delete_by_id(self, lobby_id):
        self.lobby_repository.delete(lobby_id)

    def join_player(self, lobby_id, player_id):
        lobby = self.lobby_repository.get(lobby_id)
        lobby.add_player(player_id)
        self.lobby_repository.save(lobby)
        return lobby
