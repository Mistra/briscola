

class Player:
    id: None
    name: None
    created_at: None

    def __eq__(self, other) -> bool:
        return self.id == other.id and \
            self.name == other.name and \
            self.created_at == other.created_at
