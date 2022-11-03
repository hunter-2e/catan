import board, player as ply
import draw

board = board.Board()
Emanuel = ply.Player("Emanuel", "white")
board.setRoad(Emanuel, (4,2),(5,2))
print(board.roadsPlaced)
Hunter = ply.Player("Hunter", "red")
Chamin = ply.Player("Chamin", "blue")
Kobi = ply.Player("Kobi", "orange")


draw.drawBoard(board, draw.img)


draw.drawSettle(draw.img, Emanuel, (4,2), (5,2))
draw.drawRoad(draw.img, Emanuel, (4,2), (5,2))



    
 
    # players are given a color, and their starting pieces
    # via some method, board is setup
    # players are randomly given a starting order (or with dice rolls)
    # shuffle deck of development cards?
    # put the first 2 settling turns in here or main loop?

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
