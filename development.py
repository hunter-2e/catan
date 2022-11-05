import random

class devCard:
    def __init__(self):
        self.devDeck = {
            "KnightCard":       14,
            "RoadBuilding":     2,
            "YearOfPlenty":     2,
            "Monopoly":         2,
            "VictoryPointCard": 5,    }

    def buyDevCard(self, player):
        boughtCard = random.choice(list(self.devDeck))
        player.unusedDevelopmentCards[boughtCard] += 1
        self.devDeck[boughtCard] -= 1

    def playKnightCard(self, board, player, newLocation):
        if player.unusedDevelopmentCards["KnightCard"] < 1:
            return False
        player.unusedDevelopmentCards["KnightCard"] -= 1
        
        board.moveRobber(newLocation)
        
