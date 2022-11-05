class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.victoryPoints          = 0
        self.settlementQuantity     = 5
        self.cityQuantity           = 4
        self.roadQuantity           = 15
        self.settlementSpots = []
        self.citySpots = []
        self.roadsPlaced = []
        
        self.currentResources       = {
            "brick":  0,
            "wood": 0,
            "rock":    0,
            "wheat":  0,
            "sheep":   0,              }

        self.unusedDevelopmentCards = {
            "KnightCard":       0,
            "RoadBuilding":     0,
            "YearOfPlenty":     0,
            "Monopoly":         0,
            "VictoryPointCard": 0,    }

        self.usedDevelopmentCards   = {
            "KnightCard":       0,
            "RoadBuilding":     0,
            "YearOfPlenty":     0,
            "Monopoly":         0,
            "VictoryPointCard": 0,    }


    # quantity should be an integer
    def modvictQuantity(self, quantity):
        if self.victoryPoints + quantity >= 0: 
            self.victoryPoints += quantity
        else:
            raise ValueError("cannot modify victory points")

    # quantity should be an integer
    def modSettQuantity(self, quantity):
        if self.settlementQuantity + quantity >= 0 and self.settlementQuantity + quantity <= 5: 
            self.settlementQuantity += quantity
        else:
            raise ValueError("cannot modify settlement quantity")

    # quantity should be a negative integer
    def modCityQuantity(self, quantity):
        if self.cityQuantity + quantity >= 0 and quantity < 0: 
            self.cityQuantity += quantity
        else:
            raise ValueError("cannot modify city quantity")

    # quantity should be a negative integer
    def modRoadQuantity(self, quantity):
        if self.roadQuantity + quantity >= 0 and quantity < 0: 
            self.roadQuantity += quantity
        else:
            raise ValueError("cannot modify road quantity")

    # quantity should be an integer
    # resource should be a string, either: "Brick", "Lumber", "Ore", "Grain", or "Wool"
    def modCurrResource(self, resource, quantity):
        if self.currentResources[resource] + quantity >= 0: 
            self.currentResources[resource] += quantity
        else:
            raise ValueError("cannot modify resource")

    # quantity should be an integer
    # resource should be a string, either: "KnightCard", "RoadBuilding", "YearOfPlenty", "Monopoly", or "VictoryPointCard"
    def modUnusedDev(self, card, quantity):
        if self.unusedDevelopmentCards[card] + quantity >= 0: 
            self.unusedDevelopmentCards[card] += quantity
        else:
            raise ValueError("cannot modify unused development cards")

    # quantity should be a positive integer
    # resource should be a string, either: "KnightCard", "RoadBuilding", "YearOfPlenty", "Monopoly", or "VictoryPointCard"
    def modUsedDev(self, card, quantity):
        if self.usedDevelopmentCards[card] + quantity >= 0 and quantity > 0: 
            self.usedDevelopmentCards[card] += quantity
        else:
            raise ValueError("cannot modify used development cards")

    def hasResource(self, resource: str, quantity: int) -> bool:
        """Checks if the player has the given resource and quantity.
        
        Returns:
            True if they have the resource, false if they do not.
        """

        if self.currentResources[resource] >= quantity:
            return True

        return False

