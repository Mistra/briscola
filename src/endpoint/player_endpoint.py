

import logging

from flask import Blueprint, jsonify, request
from src.model.player import Player
from src.service.player_service import PlayerService

player_endpoint = Blueprint('player_endpoint', __name__)


@player_endpoint.route('/', methods=["GET"])
def get_all():
    player_service = PlayerService()
    players = player_service.get_all()
    return jsonify([player.__dict__ for player in players])


@player_endpoint.route('/<player_id>', methods=["GET"])
def get_by_id(player_id):
    player_service = PlayerService()
    player = player_service.get_by_id(player_id)
    return jsonify(player.__dict__)


@player_endpoint.route('/', methods=["POST"])
def create():
    player_service = PlayerService()
    data = request.json
    logging.debug("Creating player: %s", data)
    player = player_service.create(Player(id=None, name=data['name']))
    return jsonify(player.__dict__)
