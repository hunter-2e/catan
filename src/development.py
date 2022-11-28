import random

def buyDevCard(player, devDeck) -> str:
    possibleDevCards = []
    for card in devDeck:
        if devDeck[card] > 0:
            possibleDevCards.append(card)
    
    boughtCard = random.choice(list(possibleDevCards))

    player.unusedDevelopmentCards[boughtCard] += 1
    devDeck[boughtCard] -= 1

    return boughtCard

def playKnightCard(ctrl, player, newLocation, playerToRob):
    if player.unusedDevelopmentCards["KnightCard"] < 1:
        raise Exception("You do not have a knight card to play.")

    player.unusedDevelopmentCards["KnightCard"] -= 1
    player.usedDevelopmentCards["KnightCard"] += 1

    try:
        ctrl.move_robber(newLocation, playerToRob)
    except Exception as e:
        player.unusedDevelopmentCards["KnightCard"] += 1
        player.usedDevelopmentCards["KnightCard"] -= 1
        print(e)
        raise e


def playRoadBuilding(board, player, firstRoad, secondRoad):
    if player.unusedDevelopmentCards["RoadBuilding"] < 1:
        raise Exception("You do not have a road building card to play.")

    player.unusedDevelopmentCards["RoadBuilding"] -= 1

    board.setRoad(player, firstRoad[0], firstRoad[1])
    board.setRoad(player, secondRoad[0], secondRoad[1])



def playYearOfPlenty(controller, player, materialOne, materialTwo):
    if player.unusedDevelopmentCards["YearOfPlenty"] < 1:
        raise Exception("You do not have a year of plenty card to play.")

    if controller.resource_bank[materialOne] < 1 or controller.resource_bank[materialTwo] < 1:
        raise Exception("Resource bank does not have the necessary resources.")

    player.unusedDevelopmentCards["YearOfPlenty"] -= 1
    
    controller.resource_bank[materialOne] -= 1
    player.currentResources[materialOne] += 1

    controller.resource_bank[materialTwo] -= 1
    player.currentResources[materialTwo] += 1

def playMonopoly(controller, player, chosenMaterial):
    if player.unusedDevelopmentCards["Monopoly"] < 1:
        raise Exception("You do not have a monopoly card to play.")

    player.unusedDevelopmentCards["Monopoly"] -= 1

    stolenItemAmount = 0
    #Change controller for controller.players
    for otherPlayers in controller.players:
        if otherPlayers.name != player.name:
            stolenItemAmount += otherPlayers.currentResources[chosenMaterial]

            otherPlayers.currentResources[chosenMaterial] = 0
    player.currentResources[chosenMaterial] += stolenItemAmount

def playVictoryPointCard(player):
    player.victoryPoints += 1
