import random
from uuid import uuid4 as uuid


class BootstrapUtils:
    @staticmethod
    def roll_players_turns(player_ids: list[uuid]) -> list[uuid]:
        random.shuffle(player_ids)
        return player_ids

    @staticmethod
    def roll_turn_sequence(number_of_players: int, rnd=random) -> list[int]:
        turns = list(range(number_of_players))
        random_shift = rnd.randrange(0, number_of_players)
        return turns[random_shift:] + turns[:random_shift]
