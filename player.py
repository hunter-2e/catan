class Chamin:
    def __init__(self, name):
        self.name = name

        self.victoryPoints          = 0
        self.settlementQuantity     = 5
        self.cityQuantity           = 4
        self.roadQuantity           = 15
        
        self.currentResources       = {
            "Brick":  0,
            "Lumber": 0,
            "Ore":    0,
            "Grain":  0,
            "Wool":   0,              }

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


player1 = Chamin("Chamin")
#player1.modCurrResource("Brick", 1)
#player1.modSettQuantity(-1)
#player1.modRoadQuantity(-1)
print()
print("name:               " + player1.name)
print("victory points:     " + str(player1.victoryPoints))
print("settlemet quantity: " + str(player1.settlementQuantity))
print("city quantity:      " + str(player1.cityQuantity))
print("road quantity:      " + str(player1.roadQuantity))
print("current Resources:  " + str(player1.currentResources))
print("unused dev cards    " + str(player1.unusedDevelopmentCards))
print("used dev cards      " + str(player1.usedDevelopmentCards))
print()