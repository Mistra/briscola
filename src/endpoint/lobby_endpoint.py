

import logging

from flask import Blueprint, jsonify
from src.model.lobby import Lobby
from src.service.lobby_service import LobbyService

lobby_endpoint = Blueprint('lobby_endpoint', __name__)


@lobby_endpoint.route('/', methods=["GET"])
def get_all():
    logging.debug("Received request to get all lobbies")
    lobby_service = LobbyService()
    lobbies = lobby_service.get_all()
    return jsonify([lobby.__dict__ for lobby in lobbies])


@lobby_endpoint.route('/<lobby_id>', methods=["GET"])
def get_by_id(lobby_id):
    logging.debug("Recieved request to get lobby with id %s", lobby_id)
    lobby_service = LobbyService()
    lobby = lobby_service.get_by_id(lobby_id)
    return jsonify(lobby.__dict__)


@lobby_endpoint.route('/', methods=["POST"])
def create():
    logging.debug("Received lobby creation request")
    lobby_service = LobbyService()
    lobby = lobby_service.create(Lobby(id=None))
    return jsonify(lobby.__dict__)


@lobby_endpoint.route('<lobby_id>/add-player/<player_id>', methods=["POST"])
def add_player(lobby_id, player_id):
    logging.debug("Received request to add player %s to lobby %s",
                  player_id, lobby_id)
    lobby_service = LobbyService()
    lobby_service.add_player(lobby_id, player_id)
    return jsonify({'status': 'ok'})
