#import board, player as ply
#import draw
import hikari_bot.bot as bot
import player
from typing import Union
#import game as gm
import hikari_bot.commands.accept as accept
import asyncio

#board = board.Board()
#Emanuel = ply.Player("Emanuel", "white")
#board.setRoad(Emanuel, (4,2),(5,2))
#print(board.roadsPlaced)
#Hunter = ply.Player("Hunter", "red")
#Chamin = ply.Player("Chamin", "blue")
#Kobi = ply.Player("Kobi", "orange")


#draw.drawBoard(board, draw.img)


#draw.drawSettle(draw.img, Emanuel, (4,2), (5,2))
#draw.drawRoad(draw.img, Emanuel, (4,2), (5,2))

class Game:
    """Handles all tasks related to the core functionality of the game."""

    def __init__(self) -> None:
        # store deck of dev card here?
        # store piles of resource cards here?
        # store list of players here?

        self.resource_bank = {
            "Brick": 19,
            "Wood": 19,
            "Rock": 19,
            "Wheat": 19,
            "Sheep": 19
        }

        self.active_trades = []
        self.players = []

    def get_player(self, name: str) -> player.Player:
        """Returns the player object given a name OR raises an error if none found."""

        #print(name)
        #print(self.players)
        for p in self.players:
            #print(p.name)
            if p.name == name:
                return p

        raise Exception("Player not found!")

def setup() -> Game:
    """Handles all game setup."""
 
    # players are given a color, and their starting pieces
    # via some method, board is setup
    # players are randomly given a starting order (or with dice rolls)
    # shuffle deck of development cards?
    # put the first 2 settling turns in here or main loop?

    game = Game()

    test1 = player.Player("KobiTheKing", "blue")
    game.players.append(test1)
    test2 = player.Player("Hunter2e", "orange")
    game.players.append(test2)

    return game

def run():
    """Controls the main game loop."""
    # loop through each player until someone wins
    # player is forced to roll at the start of their turn, resource cards are automatically distributed
    # if a 7 is rolled handle robber stuff
    # player is then allowed to trade, play up to 1 development card, and build as much as they want in any order until they end their turn
    # upon every relevent action, checking if the player has won needs to happen: building city/settlement/development card or recieving largest army/longest road

def game_over():
    """Handles any cleanup that needs to occur when a player wins the game."""
    ...

def build() -> None:
        """Maybe split this into seprate methods for each building?"""
        ...

def trade(game: Game, player1: player.Player, player2: Union[player.Player, str], player1_resources: dict, player2_resources: dict) -> None:
    """Handles a trade.
    
    Raises:
        Resource Exception: If a player does not have a resource necessary to complete the trade.
    """
    # TODO: make the exception more specific
    # TODO: need to add checks to verify the trade is valid: cannot give away cards, cannot trade like cards (i.e. 2 wool for 1 wool)

    # Special case: trading to the bank with a harbor
    # TODO: add this

    # Need to check that all resources are available to trade before officially trading any cards
    for resource, num in player1_resources.items():
        if not player1.hasResource(resource, num):
            raise Resource(f"Player: {player1.name} does not have {num} {resource}")

    for resource, num in player2_resources.items():
        # Special case: trading to the bank
        if type(player2) is str and player2 == "bank":
            if game.resource_bank[resource] < num:
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
            game.resource_bank[resource] -= num
            player1.modCurrResource(resource, num)
            continue
        
        player2.modCurrResource(resource, num * -1)
        player1.modCurrResource(resource, num)

class Resource(Exception):
    """Custom exception representing when a player does not have a resource."""
    pass