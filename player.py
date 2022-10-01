class Chamin:
    def __init__(self, name):
        self.name = name

        self.settlementQuantity = 5
        self.cityQuantity       = 4
        self.roadQuantity       = 15
        self.currentResources   = {
            "Brick":  0,
            "Lumber": 0,
            "Ore":    0,
            "Grain":  0,
            "Wool":   0,
        }

    def modSettQuantity(self, quantity):
        if self.settlementQuantity + quantity >= 0 and self.settlementQuantity + quantity <= 5: 
            self.settlementQuantity += quantity
        else:
            raise ValueError("cannot modify settlement quantity")

    def modCurrResource(self, resource, quantity):
        if self.currentResources[resource] + quantity >= 0: 
            self.currentResources[resource] += quantity
        else:
            raise ValueError("cannot modify resource")


player1 = Chamin("Chamin")
#player1.modCurrResource("Brick", 1)
#player1.modSettQuantity(-1)
print()
print("name:               " + player1.name)
print("settlemet quantity: " + str(player1.settlementQuantity))
print("city quantity:      " + str(player1.cityQuantity))
print("road quantity:      " + str(player1.roadQuantity))
print("current Resources:  " + str(player1.currentResources))
print()