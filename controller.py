import board, player as ply
import draw
#import hikari_bot.bot as bot
import player
from typing import Union
import development
import asyncio
import random

board = board.Board()
devDeck = development.devCard()

Emanuel = ply.Player("Emanuel", "white")
Hunter = ply.Player("Hunter", "red")
Chamin = ply.Player("Chamin", "blue")
Kobi = ply.Player("Kobi", "orange")

players = [Emanuel, Kobi, Hunter, Chamin]
board.setSettlement(Hunter, (0,0), 1)
print(board.settleOnTile)
board.getMaterial(players, 6)
print(Hunter.currentResources)

class Controller:
    """Handles all tasks related to the core functionality of the game."""

    def __init__(self) -> None:
        # store deck of dev card here?

        self.resource_bank = {
            "brick": 19,
            "wood": 19,
            "rock": 19,
            "wheat": 19,
            "sheep": 19
        }

        self.active_trades = []
        self.players = []
        self.current_player = 0     # Index in self.players of the player whose turn it is

    def trade(self, trade_num: int, player2: Union[player.Player, str]) -> None:
        """Handles a trade.

        Raises:
            Resource Exception: If a player does not have a resource necessary to complete the trade.
        """
        # TODO: need to add checks to verify the trade is valid: cannot give away cards, cannot trade like cards (i.e. 2 wool for 1 wool)

        # Special case: trading to the bank with a harbor
        # TODO: add this

        player1 = self.get_player(self.active_trades[trade_num - 1]["name"])
        player1_resources = self.active_trades[trade_num - 1]["p1_out"]
        player2_resources = self.active_trades[trade_num - 1]["p2_in"]

        # Need to check that all resources are available to trade before officially trading any cards
        for resource, num in player1_resources.items():
            if not player1.hasResource(resource, num):
                raise Resource(f"Player: {player1.name} does not have {num} {resource}")

        for resource, num in player2_resources.items():
            # Special case: trading to the bank
            if type(player2) is str and player2 == "bank":
                if self.resource_bank[resource] < num:
                    raise Resource(f"Bank does not have {num} {resource}")
                continue

            if not player2.hasResource(resource, num):
                raise Resource(f"Player: {player2.name} does not have {num} {resource}")

        for resource, num in player1_resources.items():
            player1.modCurrResource(resource, num * -1)
            player2.modCurrResource(resource, num)

        for resource, num in player2_resources.items():
            # Special case: trading to the bank
            if type(player2) is str and player2 == "bank":
                self.resource_bank[resource] -= num
                player1.modCurrResource(resource, num)
                continue
            
            player2.modCurrResource(resource, num * -1)
            player1.modCurrResource(resource, num)

    def build(self, player: str, building: str, location_1: str, location_2: Union[str, None]) -> None:
        """Maybe split this into seperate methods for each building?

        Raises:
            Resource Exception: If a player does not have a resource necessary to complete the trade.
        """
        
        player_obj = self.get_player(player)

        if building == "Road":
            if not player_obj.hasResource("wood", 1) or not player_obj.hasResource("brick", 1):
                raise Resource(f"Player: {player_obj.name} does not have the necessary resources.")
        elif building == "Settlement":
            ...
        elif building == "City":
            ...
        elif building == "Development Card":
            ...

    def moveRobber(self) -> None:
        """Moves the robber."""
        ...

    def activateDevCard(self, card) -> None:
        """Handled the activation of a development card."""
        ...

    def hasWon(self) -> None:
        """Checks if a given player has won"""
        # not sure if we want to keep a running total that we just add to after each action a player makes or if we want to have this method here to check all relevent stuffs to see if a player has won

    def rollDice(self) -> tuple:
        """Rolls 2 dice randomly.
        
        Returns:
            The 2 dice rolls.
        """

        return (random.randint(1, 6), random.randint(1, 6))

    def get_player(self, name: str) -> player.Player:
        """Returns the player object given a name OR raises an error if none found."""

        for p in self.players:
            if p.name == name:
                return p

        raise Exception("Player not found!")

def setup() -> Controller:
    """Handles all game setup."""
 
    # players are given a color, and their starting pieces
    # via some method, board is setup
    # players are randomly given a starting order (or with dice rolls)
    # shuffle deck of development cards?
    # put the first 2 settling turns in here or main loop?

    ctrl = Controller()

    test1 = player.Player("KobiTheKing", "blue")
    ctrl.players.append(test1)
    test1.modCurrResource("brick", 1)
    test2 = player.Player("Hunter2e", "orange")
    ctrl.players.append(test2)
    test2.modCurrResource("lumber", 2)

    return ctrl

async def run(ctrl: Controller) -> None:
    """Controls the main game loop."""
    # loop through each player until someone wins
    # player is forced to roll at the start of their turn, resource cards are automatically distributed
    # if a 7 is rolled handle robber stuff
    # player is then allowed to trade, play up to 1 development card, and build as much as they want in any order until they end their turn
    # upon every relevent action, checking if the player has won needs to happen: building city/settlement/development card or recieving largest army/longest road

    while not ctrl.hasWon():
        
        # Empty active trades list at end of each turn
        ctrl.active_trades = []

        if ctrl.current_player == len(ctrl.players) - 1:
            ctrl.current_player = 0
        else:
            ctrl.current_player += 1

        await asyncio.sleep(20)

def game_over():
    """Handles any cleanup that needs to occur when a player wins the game."""
    ...

class Resource(Exception):
    """Custom exception representing when a player does not have a resource."""
    pass