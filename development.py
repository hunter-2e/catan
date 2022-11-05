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
        possibleDevCards = []
        for card in self.devDeck:
            if self.devDeck[card] > 0:
                possibleDevCards.append(card)
        
        boughtCard = random.choice(list(possibleDevCards))

        player.unusedDevelopmentCards[boughtCard] += 1
        self.devDeck[boughtCard] -= 1



    def playKnightCard(self, board, player, newLocation, playerToRob):
        if player.unusedDevelopmentCards["KnightCard"] < 1:
            return False

        player.unusedDevelopmentCards["KnightCard"] -= 1
        board.moveRobber(newLocation)

        for tile in board.settleOnTile:
            if '(' + str(board.robberLocation[0]) + ',' + str(board.robberLocation[1]) + ')' in tile:
                if playerToRob.name + "'s Settlement" or playerToRob.name + "'s City" in board.settleOnTile[tile]:
                    possibleStolenCards = []
                    for card in playerToRob.currentResources:
                        if playerToRob.currentResources[card] > 0:
                            possibleStolenCards.append(card)
                    
                    if(len(possibleStolenCards) == 0):
                        return False

                    stolenCard = random.choice(possibleStolenCards)

                    playerToRob.currentResources[stolenCard] -= 1
                    player.currentResources[stolenCard] += 1
    
    def playRoadBuilding(self, board, player, firstRoad, secondRoad):
        
