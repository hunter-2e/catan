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
            "Brick": 19,
            "Wood": 19,
            "Rock": 19,
            "Wheat": 19,
            "Sheep": 19
        }

        self.active_trades = []
        self.players = []

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

        print(name)
        print(self.players)
        for p in self.players:
            print(p.name)
            if p.name == name:
                return p

        raise Exception("Player not found!")