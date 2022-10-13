import random

import player

class Game:
    def __init__(self) -> None:
        # store deck of dev card here?
        # store piles of resource cards here?
        # store list of players here?
        pass

    def build(self) -> None:
        """Maybe split this into seprate methods for each building?"""
        ...

    def trade(self, player1: player.Player, player2: player.Player, player1_resources: dict, player2_resources: dict) -> None:
        """Handles a trade.
        
        Raises:
            Exception: If a player does not have any of the resources necessary to complete the trade.
        """
        # TODO: make the exception more specific

        for resource, num in player1_resources.items():
            if not player1.hasResource(resource, num):
                raise Exception(f"Player: {player1.name} does not have {num} {resource}")

        for resource, num in player2_resources.items():
            if not player2.hasResource(resource, num):
                raise Exception(f"Player: {player2.name} does not have {num} {resource}")

        for resource, num in player1_resources.items():
            player1.modCurrResource(resource, num)

        for resource, num in player2_resources.items():
            player2.modCurrResource(resource, num)

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