from typing import Union
import asyncio
import random

import hikari

import src.board as board
import src.hikari_bot.bot as bot
import src.player as player
import src.development as development
import src.hikari_bot.bot as bot

class Controller:
    """Handles all tasks related to the core functionality of the game."""

    def __init__(self, dev_deck) -> None:
        # store deck of dev card here?

        self.resource_bank = {
            "brick": 19,
            "wood": 19,
            "rock": 19,
            "wheat": 19,
            "sheep": 19
        }

        self.board = None
        self.active_trades = []
        self.players = []
        self.current_player = 0     # Index in self.players of the player whose turn it is
        self.dev_deck = dev_deck
        self.flag = None
        self.cur_dice = None
        self.has_robber_moved = False

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

            self.board.setSettlement(self.players, player_obj, location_1, 1)

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

            self.dev_deck.buyDevCard(player_obj)

            player_obj.modCurrResource("wheat", -1)
            player_obj.modCurrResource("rock", -1)
            player_obj.modCurrResource("sheep", -1)

        #bot.send_image_or_message("test.png", None)

    def move_robber(self, new_location: tuple, player_to_rob: str) -> str:
        """Moves the robber."""
        
        player_to_rob = self.get_player(player_to_rob)
        self.board.moveRobber(new_location)
        stolenCard = None

        for tile in self.board.settleOnTile:
            if '(' + str(self.board.robberLocation[0]) + ',' + str(self.board.robberLocation[1]) + ')' in tile:
                if player_to_rob.name + "'s Settlement" or player_to_rob.name + "'s City" in self.board.settleOnTile[tile]:
                    possibleStolenCards = []
                    for card in player_to_rob.currentResources:
                        if player_to_rob.currentResources[card] > 0:
                            possibleStolenCards.append(card)
                    
                    if(len(possibleStolenCards) == 0):
                        raise Exception(f"{player_to_rob} does not have any cards to steal.")

                    stolenCard = random.choice(possibleStolenCards)

                    player_to_rob.currentResources[stolenCard] -= 1
                    self.players[self.current_player].currentResources[stolenCard] += 1

        return stolenCard

    def activate_dev_card(self, card) -> None:
        """Handled the activation of a development card."""
        ...

    def has_won(self) -> None:
        for player in self.players:
            if player.victoryPoints == 10:
                return True

    def roll_dice(self) -> int:
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

    dev_deck = development.devCard()
    ctrl = Controller(dev_deck)

    return ctrl

async def run(ctrl: Controller, flag: asyncio.Event, drawing_mode: str) -> None:
    """Controls the main game loop."""
    # loop through each player until someone wins
    # player is forced to roll at the start of their turn, resource cards are automatically distributed
    # if a 7 is rolled handle robber stuff
    # player is then allowed to trade, play up to 1 development card, and build as much as they want in any order until they end their turn
    # upon every relevent action, checking if the player has won needs to happen: building city/settlement/development card or recieving largest army/longest road

    #TMP TEST SENDING IMAGE
    #await bot.send_image("test.png")

    ctrl.board = board.Board(drawing_mode)

    ctrl.flag = flag

    while not ctrl.has_won():
        ctrl.has_robber_moved = False
        ctrl.flag.clear()
        ctrl.active_trades = []     # emptied at start of each turn

        ctrl.cur_dice = ctrl.roll_dice()
        message = hikari.Embed(title=f"{ctrl.players[ctrl.current_player].name}'s turn",
                description=f"Dice roll: {ctrl.cur_dice}",
                color=hikari.Color(0x00FF00)
        )
        await bot.send_image_or_message(None, message)

        await bot.send_image_or_message("images/test.png", None)
        
        if ctrl.cur_dice == 7:
            # Prompt user user for new robber location, wait for response
            await bot.send_image_or_message(None, "Use /rob <location> <player> to move the robber and steal from someone.")

            await ctrl.flag.wait()

            ctrl.flag.clear()
            ctrl.has_robber_moved = True
        else:
            ctrl.board.getMaterial(ctrl.players, ctrl.cur_dice)  # give all players their materials based on the roll of the dice

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