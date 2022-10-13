import random

class Game:
    def __init__(self) -> None:
        # store deck of dev card here?
        # store piles of resource cards here?
        # store list of players here?
        pass

    def build() -> None:
        """Maybe split this into seprate methods for each building?"""
        ...

    def trade() -> None:
        """Handles a trade."""
        ...

    def move_robber() -> None:
        """Moves the robber."""
        ...

    def activate_dev_card(card) -> None:
        """Handled the activation of a development card."""
        ...

    def has_one() -> None:
        """Checks if a given player has won"""
        # not sure if we want to keep a running total that we just add to after each action a player makes or if we want to have this method here to check all relevent stuffs to see if a player has won

    def roll_dice() -> tuple:
        """Rolls 2 dice randomly.
        
        Returns:
            The 2 dice rolls.
        """

        return (random.randint(1, 6), random.randint(1, 6))