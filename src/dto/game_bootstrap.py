

from datetime import datetime
from uuid import uuid4 as uuid

from src.model.game import Game


class GameBootstrap:
    game: Game
    player_id: uuid
    creation_time: datetime
