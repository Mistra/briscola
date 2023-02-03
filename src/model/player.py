from datetime import datetime
from uuid import uuid4


class Player:
    def __init__(
        self, player_id: uuid4 = None, name: str = None, created_at: datetime = None
    ):
        self.id: uuid4 = player_id
        self.name: str = name
        self.created_at: datetime = created_at

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.created_at == other.created_at
        )
