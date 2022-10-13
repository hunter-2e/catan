import random
from typing import Union

import player

class Game:
    """Handles all tasks related to the core functionality of the game."""

    def __init__(self) -> None:
        # store deck of dev card here?
        # store piles of resource cards here?
        # store list of players here?

        self.resource_bank = {
            "Brick":  19,
            "Lumber": 19,
            "Ore":    19,
            "Grain":  19,
            "Wool":   19
        }

    def build(self) -> None:
        """Maybe split this into seprate methods for each building?"""
        ...

    def trade(self, player1: player.Player, player2: Union[player.Player, str], player1_resources: dict, player2_resources: dict) -> None:
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
                if self.resource_bank[resource] < num:
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
                self.resource_bank[resource] -= num
                player1.modCurrResource(resource, num)
                continue
            
            player2.modCurrResource(resource, num * -1)
            player1.modCurrResource(resource, num)

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