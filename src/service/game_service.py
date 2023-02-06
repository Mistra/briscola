import logging
import random
from datetime import datetime
from typing import List, Optional
from uuid import uuid4 as uuid

from src.dto.game_state import GameState
from src.model.card import CardSuit
from src.model.deck import Deck
from src.model.game import Game
from src.model.game_player import GamePlayer
from src.model.hand import Hand
from src.model.stack import Stack
from src.repository.game_player_repository import GamePlayerRepository
from src.repository.game_repository import GameRepository
from src.repository.game_state_repository import GameStateRepository
from src.service.bootstrap_utils import BootstrapUtils


class GameService:
    def __init__(
        self,
        game_repository: GameRepository = None,
        game_player_repository: GamePlayerRepository = None,
        game_state_repository: GameStateRepository = None,
    ):
        self.datetime = datetime
        self.id_generator = uuid
        self.random = random
        self.game_repository = game_repository
        self.game_state_repository = game_state_repository
        self.game_player_repository = game_player_repository

    def create(self, player_id: uuid):
        logging.debug("Setting up the game for player: %s", player_id)

        game = Game()
        game.id = str(self.id_generator())
        game.created_at = datetime.utcnow()

        self.game_repository.create(game)

    def join(self, player_id: uuid, game_id: uuid):
        number_of_players = 2

        game_player = GamePlayer()
        game_player.id = self.id_generator()
        game_player.player_id = player_id
        game_player.game_id = game_id

        self.game_player_repository.create(game_player, number_of_players)

    def bootstrap(self, game_id: uuid, deck: Optional[Deck] = None):
        number_of_players = 2
        game = self.__initialize_game(game_id, deck)
        player_stacks = self.__create_player_stacks(number_of_players, game_id)
        player_hands = self.__create_hands(number_of_players, game)

        game_state = GameState()
        game_state.game = game
        game_state.player_stacks = player_stacks
        game_state.player_hands = player_hands

        self.game_state_repository.save(game_state)

    def play_card(self, player_id, game_id, card):
        hand = Hand(game_id=game_id, player_id=player_id, played_card=card)

        game_state = GameState()
        game_state.player_hands = [hand]

        self.game_state_repository.update(game_state)

    def fetch_state(self, game_id):
        pass

    def fetch_state_for_player(self, game_id, player_id):
        # check what's in player's hands
        # check what's player's turn
        # check what's in table
        # check what's in stack
        # check last played hand
        # check deck (number of cards and briscola/last)
        pass

    def __create_player_stacks(
        self, number_of_players: int, game_id: str
    ) -> list[Stack]:
        stacks: list[Stack] = []

        for _ in range(number_of_players):
            stack = Stack()

            stack.id = str(self.id_generator())
            stack.game_id = game_id
            stack.cards = []

            stacks.append(stack)

        return stacks

    def __create_hands(self, number_of_players: int, game: Game) -> list[Hand]:
        hands: list[Hand] = []
        turns = BootstrapUtils.roll_turn_sequence(number_of_players, self.random)

        for idx in range(number_of_players):
            hand = Hand()

            hand.id = str(self.id_generator())
            hand.updated_at = self.datetime.utcnow()
            hand.game_id = game.id
            hand.turn = turns[idx]
            hand.cards = game.cards.pick(3)

            hands.append(hand)

        return hands

    def __initialize_game(self, game_id: str, deck: Deck) -> Game:
        game = Game()

        game.id = game_id
        game.cards = Deck.init_shuffled() if deck is None else deck

        return game

    @staticmethod
    def __move_is_valid(
        current_game_state: GameState, new_game_state: GameState
    ) -> bool:
        # FIXME: horrific dto abuse, use player_move
        player_id = new_game_state.player_hands[0].player_id
        played_card = new_game_state.player_hands[0].played_card
        sorted_hands = sorted(
            current_game_state.player_hands, key=lambda hand: hand.turn
        )

        # check if it's player's turn
        for hand in sorted_hands:
            if hand.player_id == player_id:  # it's player's turn
                break
            if hand.played_card is None:  # someone before player didn't play
                return False

        # check if player owns played card
        player_hand = next(
            (hand for hand in sorted_hands if hand.player_id == player_id), None
        )
        return player_hand is not None and player_hand.played_card == played_card

    @staticmethod
    def __update_game_state(
        current_game_state: GameState, new_game_state: GameState
    ) -> GameState:
        # FIXME: horrific dto abuse, use player_move
        player_id = new_game_state.player_hands[0].player_id
        played_card = new_game_state.player_hands[0].played_card
        number_of_players = current_game_state.get_number_of_players()
        player_hand = current_game_state.get_player_hand(player_id)

        # updating current_game_state
        player_hand.played_card = played_card

        if player_hand.turn == number_of_players - 1:
            return GameService.__cycle_hands(current_game_state)
        return current_game_state

    @staticmethod
    def __cycle_hands(game_state: GameState) -> GameState:
        hands = game_state.player_hands
        # FIXME: problem, when last card is picked up there's no way to tell what's trump
        winning_hand = GameService.__calculate_winning_hand(
            hands, game_state.game.cards[-1]
        )
        played_cards = list(map(lambda hand: hand.played_card, hands))
        winning_stack = game_state.get_player_stack(winning_hand.player_id)
        winning_stack.cards.extend(played_cards)

        for hand in hands:
            hand.cards.remove(hand.played_card)
            hand.played_card = None

        # TODO: give winner turn 0 and pick next card from deck
        return game_state

    @staticmethod
    def __calculate_winning_hand(hands: List[Hand], trump_suit: CardSuit) -> Hand:
        """Given a hand of cards, calculate the winning hand"""
        if len(hands) == 0:
            raise ValueError("No cards")

        trump_hands = list(filter(lambda hand: hand.played_card == trump_suit, hands))
        winning_suit = (
            trump_hands[0].played_card.suit
            if len(trump_hands) > 0
            else hands[0].played_card.suit
        )

        filtered_hands = filter(
            lambda hand: hand.played_card.suit == winning_suit, hands
        )
        return max(filtered_hands, key=lambda hand: hand.played_card.value)
