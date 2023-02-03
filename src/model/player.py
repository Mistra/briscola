from datetime import datetime
from uuid import uuid4


class Player:
    def __init__(self):
        self.id: uuid4 = None
        self.name: str = None
        self.created_at: datetime = None

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.created_at == other.created_at
        )
