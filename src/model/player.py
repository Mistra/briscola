

from datetime import datetime
from uuid import uuid4


class Player:
    id: uuid4
    name: str
    created_at: datetime

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.name == other.name and \
            self.created_at == other.created_at
