import board, player as ply
import draw
import hikari_bot.bot as bot
import player
from typing import Union
import development
import asyncio
import random
import hikari

#board = board.Board()
#devDeck = development.devCard()

#Emanuel = ply.Player("Emanuel", "white")
#Hunter = ply.Player("Hunter", "red")
#Chamin = ply.Player("Chamin", "blue")
#Kobi = ply.Player("Kobi", "orange")

#players = [Emanuel, Kobi, Hunter, Chamin]

class Controller:
    """Handles all tasks related to the core functionality of the game."""

    def __init__(self, board, dev_deck) -> None:
        # store deck of dev card here?

        self.resource_bank = {
            "brick": 19,
            "wood": 19,
            "rock": 19,
            "wheat": 19,
            "sheep": 19
        }

        self.board = board
        self.active_trades = []
        self.players = []
        self.current_player = 0     # Index in self.players of the player whose turn it is
        self.dev_deck = dev_deck
        self.flag = None

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

    def build(self, player: str, building: str, location_1: tuple, location_2: Union[tuple, None]) -> None:
        """Maybe split this into seperate methods for each building?

        Raises:
            Resource Exception: If a player does not have a resource necessary to complete the trade.
        """
        
        player_obj = self.get_player(player)

        if building == "Road":
            # TODO: STILL NEED TO ADD CHECKER FOR IF THE ROAD LOCATIONS ARE VALID OR NOT

            if not player_obj.hasResource("wood", 1) or not player_obj.hasResource("brick", 1):
                raise Resource(f"Player: {player_obj.name} does not have the necessary resources.")

            self.board.setRoad(player_obj, location_1, location_2)

            player_obj.modCurrResource("wood", -1)
            player_obj.modCurrResource("brick", -1)
        elif building == "Settlement":
            if not player_obj.hasResource("wood", 1) or not player_obj.hasResource("brick", 1) or not player_obj.hasResource("wheat", 1) or not player_obj.hasResource("sheep", 1):
                raise Resource(f"Player: {player_obj.name} does not have the necessary resources.")

            print("TEST" + str(location_1))
            print(type(location_1))
            print(self.board.setSettlement(self.players, player_obj, location_1, 1))

            player_obj.modCurrResource("wood", -1)
            player_obj.modCurrResource("brick", -1)
            player_obj.modCurrResource("wheat", -1)
            player_obj.modCurrResource("sheep", -1)
        elif building == "City":
            if not player_obj.hasResource("wheat", 2) or not player_obj.hasResource("rock", 3):
                raise Resource(f"Player: {player_obj.name} does not have the necessary resources.")

            self.board.setSettlement(self.players, player_obj, location_1, 2)

            player_obj.modCurrResource("wheat", -2)
            player_obj.modCurrResource("rock", -3)
        elif building == "Development Card":
            if not player_obj.hasResource("wheat", 1) or not player_obj.hasResource("rock", 1) or not player_obj.hasResource("sheep", 1):
                raise Resource(f"Player: {player_obj.name} does not have the necessary resources.")

            #TODO: dev card stuff here

            player_obj.modCurrResource("wheat", -1)
            player_obj.modCurrResource("rock", -1)
            player_obj.modCurrResource("sheep", -1)

        #bot.send_image_or_message("test.png", None)

    def move_robber(self, new_location, player_to_rob) -> None:
        """Moves the robber."""
        
        self.board.moveRobber(new_location)

        for tile in board.settleOnTile:
            if '(' + str(board.robberLocation[0]) + ',' + str(board.robberLocation[1]) + ')' in tile:
                if player_to_rob.name + "'s Settlement" or player_to_rob.name + "'s City" in board.settleOnTile[tile]:
                    possibleStolenCards = []
                    for card in player_to_rob.currentResources:
                        if player_to_rob.currentResources[card] > 0:
                            possibleStolenCards.append(card)
                    
                    if(len(possibleStolenCards) == 0):
                        return False

                    stolenCard = random.choice(possibleStolenCards)

                    player_to_rob.currentResources[stolenCard] -= 1
                    player.currentResources[stolenCard] += 1

    def activate_dev_card(self, card) -> None:
        """Handled the activation of a development card."""
        ...

    def has_won(self) -> None:
        """Checks if a given player has won"""
        # not sure if we want to keep a running total that we just add to after each action a player makes or if we want to have this method here to check all relevent stuffs to see if a player has won

    def roll_dice(self) -> tuple:
        """Rolls 2 dice randomly.
        
        Returns:
            The 2 dice rolls.
        """

        #return (random.randint(1, 6), random.randint(1, 6))
        return random.randint(1, 6) + random.randint(1, 6)

    def get_player(self, name: str) -> player.Player:
        """Returns the player object given a name OR raises an error if none found."""

        for p in self.players:
            if p.name == name:
                return p

        raise Exception("Player not found!")

    def add_player(self, name: str, color: str) -> None:
        """Adds a new player to the game."""

        p = player.Player(name, color)
        self.players.append(p)

def setup() -> Controller:
    """Handles all game setup."""
 
    # players are given a color, and their starting pieces
    # via some method, board is setup
    # players are randomly given a starting order (or with dice rolls)
    # shuffle deck of development cards?
    # put the first 2 settling turns in here or main loop?

    b = board.Board()
    dev_deck = development.devCard()
    ctrl = Controller(b, dev_deck)

    return ctrl

async def run(ctrl: Controller, flag: asyncio.Event) -> None:
    """Controls the main game loop."""
    # loop through each player until someone wins
    # player is forced to roll at the start of their turn, resource cards are automatically distributed
    # if a 7 is rolled handle robber stuff
    # player is then allowed to trade, play up to 1 development card, and build as much as they want in any order until they end their turn
    # upon every relevent action, checking if the player has won needs to happen: building city/settlement/development card or recieving largest army/longest road

    #TMP TEST SENDING IMAGE
    #await bot.send_image("test.png")

    ctrl.flag = flag

    while not ctrl.has_won():
        ctrl.flag.clear()
        ctrl.active_trades = []     # emptied at start of each turn

        dice = ctrl.roll_dice()
        message = hikari.Embed(title=f"{ctrl.players[ctrl.current_player].name}'s turn",
                description=f"Dice roll: {dice}",
                color=hikari.Color(0x00FF00)
        )
        await bot.send_image_or_message(None, message)

        await bot.send_image_or_message("test.png", None)
        
        if dice == 7:
            ctrl.move_robber()
        else:
            ctrl.board.getMaterial(ctrl.players, dice)  # give all players their materials based on the roll of the dice

        await ctrl.flag.wait()  # flag is set when play calls the /endturn command

        if ctrl.current_player == len(ctrl.players) - 1:
            ctrl.current_player = 0
        else:
            ctrl.current_player += 1



def game_over():
    """Handles any cleanup that needs to occur when a player wins the game."""
    ...

class Resource(Exception):
    """Custom exception representing when a player does not have a resource."""
    pass