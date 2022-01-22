import json
from flask import Blueprint, Response, jsonify, session
from briscola.model.lobby import Lobby
from briscola.repository.lobby_repository import LobbyRepository

from briscola.service.lobby_service import LobbyService
lobby_endpoint = Blueprint('lobby_endpoint', __name__)


@lobby_endpoint.route('/', methods=["GET"])
def get_all():
    lobby1 = Lobby()
    lobby2 = Lobby()
    lobby_repository = LobbyRepository()
    lobby_service = LobbyService(lobby_repository)
    lobby_service.create(lobby1)
    lobby_service.create(lobby2)
    lobbies = lobby_service.get_all()

    return jsonify([l.serialize() for l in lobbies])
