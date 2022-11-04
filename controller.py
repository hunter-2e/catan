import board, player as ply
import draw
#import hikari_bot.bot as bot
import player
from typing import Union
import game as gm
import development

board = board.Board()
devDeck = development.devCard()

Emanuel = ply.Player("Emanuel", "white")
Hunter = ply.Player("Hunter", "red")
Chamin = ply.Player("Chamin", "blue")
Kobi = ply.Player("Kobi", "orange")

devDeck.buyDevCard(Hunter)

draw.drawBoard(board, draw.img)

board.moveRobber((0,0))
draw.drawRoad(draw.img, Hunter, (0,0),(1,1))

draw.drawRobber(board, draw.img)
board.moveRobber((0,1))



game = gm.Game()

def setup():
    """Handles all game setup."""
 
    # players are given a color, and their starting pieces
    # via some method, board is setup
    # players are randomly given a starting order (or with dice rolls)
    # shuffle deck of development cards?
    # put the first 2 settling turns in here or main loop?

    test1 = player.Player("KobiTheKing", "blue")
    game.players.append(test1)
    test2 = player.Player("Hunter2e", "orange")
    game.players.append(test2)

    #bot.setup()

def run():
    """Controls the main game loop."""
    pass
    # loop through each player until someone wins
    # player is forced to roll at the start of their turn, resource cards are automatically distributed
    # if a 7 is rolled handle robber stuff
    # player is then allowed to trade, play up to 1 development card, and build as much as they want in any order until they end their turn
    # upon every relevent action, checking if the player has won needs to happen: building city/settlement/development card or recieving largest army/longest road
    #

def game_over():
    """Handles any cleanup that needs to occur when a player wins the game."""
    ...

def build() -> None:
        """Maybe split this into seprate methods for each building?"""
        ...

def trade(player1: player.Player, player2: Union[player.Player, str], player1_resources: dict, player2_resources: dict) -> None:
    """Handles a trade.
    
    Raises:
        Exception: If a player does not have a resource necessary to complete the trade.
    """
    # TODO: make the exception more specific
    # TODO: need to add checks to verify the trade is valid: cannot give away cards, cannot trade like cards (i.e. 2 wool for 1 wool)

    # Special case: trading to the bank with a harbor
    # TODO: add this

    # Need to check that all resources are available to trade before officially trading any cards
    for resource, num in player1_resources.items():
        if not player1.hasResource(resource, num):
            raise Exception(f"Player: {player1.name} does not have {num} {resource}")

    for resource, num in player2_resources.items():
        # Special case: trading to the bank
        if type(player2) is str and player2 == "bank":
            if game.resource_bank[resource] < num:
                raise Exception(f"Bank does not have {num} {resource}")
            continue

        if not player2.hasResource(resource, num):
            raise Exception(f"Player: {player2.name} does not have {num} {resource}")

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

#if __name__ == "__main__":
#    setup()