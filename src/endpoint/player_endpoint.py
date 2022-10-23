

import logging

import jsonpickle
from flask import Blueprint, Response, request
from src.model.player import Player
from src.service.player_service import PlayerService

player_endpoint = Blueprint('player_endpoint', __name__)


@player_endpoint.route('/<player_id>', methods=["GET"])
def get_by_id(player_id):
    player_service = PlayerService()
    player = player_service.find_by_id(player_id)

    if player is None:
        return Response(status=404)

    return Response(
        jsonpickle.encode(player, unpicklable=False, make_refs=False),
        mimetype="application/json"
    )


@player_endpoint.route('/', methods=["POST"])
def create():
    player_service = PlayerService()
    data = request.json

    logging.debug("Creating player: %s", data)
    player = Player()
    player.name = data['name']
    player = player_service.create(player)

    return Response(
        jsonpickle.encode(player, unpicklable=False, make_refs=False),
        mimetype="application/json"
    )


@player_endpoint.route('/<player_id>', methods=["DELETE"])
def delete_by_id(player_id):
    player_service = PlayerService()
    player_service.delete_by_id(player_id)
    return Response(status=204)
