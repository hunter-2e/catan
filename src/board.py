import random
import src.draw as draw
import numpy as np
from PIL import Image

class Board:
    def __init__(self, mode):
        self.setSettleCalls = 0
        self.mode = mode
        self.robberLocation = None
        #Places a settlement can be built

        self.portsSettleSpots = {
            "3for1": [(0,0), (1,0),(2,3),(3,4),(5,5),(6,5),(10,0),(11,0)],
            "Sheep": [(0,1),(1,2)],
            "Brick": [(8,4),(9,3)],
            "Rock": [(3,0),(4,0)],
            "Wheat": [(7,0),(8,0)],
            "Wood": [(10,2),(11,1)]
        }

        self.settleSpots = [[None for x in range(3)],
                      [None for x in range(4)],
                      [None for x in range(4)],
                      [None for x in range(5)],
                      [None for x in range(5)],
                      [None for x in range(6)],
                      [None for x in range(6)],
                      [None for x in range(5)],
                      [None for x in range(5)],
                      [None for x in range(4)],
                      [None for x in range(4)],
                      [None for x in range(3)]]

        self.settleOnTile = {}

        self.materialNumberTile = {}

        self.associatedPoints = [[(0,0),(1,0),(1,1),(2,0),(2,1),(3,1)],
        [(0,1),(1,1), (1,2),(2,1),(2,2), (3,2)],
         [(0,2),(1,2),(1,3),(2,2),(2,3),(3,3)], 
         [(2,0),(3,0),(3,1),(4,0),(4,1),(5,1)],
         [(2,1),(3,1),(3,2),(4,1),(4,2),(5,2)],
         [(2,2),(3,2),(3,3),(4,2),(4,3),(5,3)],
         [(2,3),(3,3),(3,4),(4,3),(4,4),(5,4)],
         [(4,0),(5,0),(5,1),(6,1),(6,0),(7,0)],
         [(4,1),(5,1),(5,2),(6,2),(6,1),(7,1)],
         [(4,2),(5,2),(5,3),(6,3),(6,2),(7,2)],
          [(4,3),(5,3),(5,4),(6,4),(6,3),(7,3)],
          [(4,4),(5,4),(5,5),(6,5),(6,4),(7,4)],
          [(6,1),(7,0),(7,1),(8,0),(8,1),(9,0)],
          [(6,2),(7,1),(7,2),(8,1),(8,2),(9,1)],
          [(6,3),(7,2),(7,3),(8,2),(8,3),(9,2)],
          [(6,4),(7,3),(7,4),(8,3),(8,4),(9,3)],
          [(8,1),(9,0),(9,1),(10,0),(10,1),(11,0)],
          [(8,2),(9,1),(9,2),(10,1),(10,2),(11,1)],
          [(8,3),(9,2),(9,3),(10,2),(10,3), (11,2)]]

        self.roadsPlaced = []

        #Places material tiles can be placed
        self.tileSpots = [[None for x in range(3)],
                        [None for x in range(4)],
                        [None for x in range(5)],
                        [None for x in range(4)],
                        [None for x in range(3)]]
        
        self.tilesAvailable = {
            'rockTile': 3,
            'brickTile': 3,
            'sheepTile': 4,
            'treeTile': 4,
            'wheatTile': 4,
            'robberTile': 1
        }

        self.numbersAvailable = {
            10: 2,
            8: 2,
            6: 2,
            2: 1,
            12: 1,
            11: 2,
            9: 2,
            3: 2,
            4: 2,
            5: 2,
            7: 1
        }
        
        #Populating tileSpots randomly with available material types and a number

        xTile = 0
        zPoints = 0
        for row in self.tileSpots:
            yTile = 0
            for tile in range(len(row)):
                 chosenTile = random.choice([tilesLeft for tilesLeft in self.tilesAvailable.keys() if self.tilesAvailable[tilesLeft] > 0])
                 
                 if chosenTile == 'robberTile':
                    chosenNum = 7
                    self.robberLocation = (xTile, yTile)
                 else:
                    chosenNum = random.choice([numLeft for numLeft in self.numbersAvailable.keys() if self.numbersAvailable[numLeft] > 0 and numLeft != 7])

                 try:
                    if(self.materialNumberTile[chosenNum] is None): 
                        self.materialNumberTile[chosenNum] = [chosenTile + '(' + str(xTile) + ',' + str(yTile) + ')']
                    else: 
                        self.materialNumberTile[chosenNum].append(chosenTile + '(' + str(xTile) + ',' + str(yTile) + ')')
                 except:
                        self.materialNumberTile[chosenNum] = [chosenTile + '(' + str(xTile) + ',' + str(yTile) + ')']

                 row[tile] = chosenTile
                 self.settleOnTile[self.tileSpots[xTile][yTile] + '(' + str(xTile) + ',' + str(yTile) + ')'] = self.associatedPoints[zPoints]

                 self.tilesAvailable[chosenTile] -= 1
                 self.numbersAvailable[chosenNum] -= 1
                 
                 yTile += 1
                 zPoints += 1
            xTile += 1
    
        draw.drawBoard(self, mode)


    def checkValidity(self, spot):
        print(spot)
        if spot[0][0] == 0 and spot[1][0] == spot[0][0] + 1 and (spot[0][1] == spot[1][1] or spot[0][1] + 1 == spot[1][1]):
            return True
        elif spot[0][0] % 2 == 0:
            if ((spot[1][0] == spot[0][0] + 1) and ((spot[0][0] < 6 and (spot[0][1] == spot[1][1] or spot[0][1] + 1 == spot[1][1])) or (spot[0][0] >= 6 and (spot[0][1] - 1 == spot[1][1] or spot[0][1] == spot[1][1])))) or (spot[0][0] - 1 == spot[1][0] and spot[0][1] == spot[1][1]):
                return True
        elif spot[0][0] == 11 and spot[1][0] == spot[0][0] - 1 and (spot[0][1] == spot[1][1] or spot[0][1] + 1 == spot[1][1]):
            return True
        else:
            if ((spot[1][0] == spot[0][0] - 1) and ((spot[0][0] > 6 and (spot[0][1] + 1 == spot[1][1] or spot[0][1] == spot[1][1])) or (spot[0][0] < 6 and (spot[0][1] - 1 == spot[1][1] or spot[0][1] == spot[1][1])))) or ((spot[1][0] == spot[0][0] + 1) and (spot[0][1] == spot[1][1])):
                return True
        return False

  
    def validRoad(self, spot, player, players):
        if spot[0] == spot[1] or ((spot[0],spot[1]) in self.roadsPlaced or (spot[1], spot[0]) in self.roadsPlaced):
            print(1)
            return False

        # being passed in ((),())
        relevantSpot = []
        
        #Add all relevant spots to build off of to array unless it is the first turn, in which case only add most recent settlement placed
        if self.setSettleCalls < len(players) * 2:
            relevantSpot.append(player.settlementSpots[-1])

        else:
            for i in player.settlementSpots:
                print(2)
                relevantSpot.append(i)
                
            for i in player.roadsPlaced:
                for j in i:
                    print(4)
                    relevantSpot.append(j)

            for i in player.citySpots:
                print(3)
                relevantSpot.append(i)

        

        maybeBuildable = False

        for i in relevantSpot:
            if spot[0] or spot[1] == i:
                maybeBuildable = True
        
        if maybeBuildable != True:
            print(2)
            return False

        for i in relevantSpot:
            if i in [spot[0], spot[1]]:
                spotInRelevant = i
        
        try:
            if spotInRelevant is None:
                return False
        except:
            return False

        if spotInRelevant == spot[0]:
            print("FIRST")
            return self.checkValidity((spotInRelevant, spot[1]))
        else:
            print("SECOND")
            return self.checkValidity((spot[0], spotInRelevant))
    

    def setRoad(self, player, spot1, spot2, players):
        spot1 = [spot1[1], spot1[0]]
        spot2 = [spot2[1], spot2[0]]

        if spot1[0] in [0,11]:
            spot1 = (spot1[0], int(((spot1[1] - 1)/2) - 1))
        elif spot1[0] in [1,2,9,10]:
            spot1 = (spot1[0], int((spot1[1]/2) - 1))
        elif spot1[0] in [3,4,7,8]:
            spot1 = (spot1[0], int((spot1[1] - 1)/2))
        else:
            spot1 = (spot1[0], int(spot1[1]/2))

        if spot2[0] in [0,11]:
            spot2 = (spot2[0], int(((spot2[1] - 1)/2) - 1))
        elif spot2[0] in [1,2,9,10]:
            spot2 = (spot2[0], int((spot2[1]/2) - 1))
        elif spot2[0] in [3,4,7,8]:
            spot2 = (spot2[0], int((spot2[1] - 1)/2))
        else:
            spot2 = (spot2[0], int(spot2[1]/2))

        #Make sure both points are settlement spots at the very least
        if self.isSpotValid(spot1) == False or self.isSpotValid(spot2):
            return False

        #If both are valid points check if road can be placed based on game's rules
        canBeBuilt = self.validRoad((spot1,spot2), player, players)
        if canBeBuilt == False:
            return False

        player.roadsPlaced.append((spot1,spot2))
        player.roadQuantity -= 1

        self.roadsPlaced.append((spot1,spot2))

        image = np.array(Image.open("images/test.png"))
        draw.drawRoad(image, player, spot1,spot2)

        return True

    def isSpotValid(self, spot):
        spotValid = False

        for row in self.associatedPoints:
            if spot in row:
                spotValid = True
                break
            
        if(spotValid is False):
            return False

    def getRoad(self, spot1, spot2):
        if([spot1, spot2] in self.roadsPlaced):
            return True
        else: return False

    def validSettlement(self, spot, player, players):
        #spots that are in the players built roads
        relevantSpots = []


        #Add each spot of road to relevant spots
        for roadSpot in player.roadsPlaced:
            relevantSpots.append(roadSpot[0])
            relevantSpots.append(roadSpot[1])

        #Check if spot to be placed is on that players road unless they haven't taken initial turns
        if self.setSettleCalls > len(players) * 2:
            if spot not in relevantSpots:
                return False


        print(spot)
        if spot[0] == 0 and self.getSettlement((spot[0] + 1, spot[1] + 1)) == None and self.getSettlement((spot[0] + 1, spot[1])) == None:
            self.setSettleCalls += 1
            return True
        elif spot[0] % 2 == 0:
            if self.getSettlement((spot[0] + 1, spot[1])) == None and self.getSettlement((spot[0] + 1, spot[1] - 1)) == None and self.getSettlement((spot[0] - 1, spot[1])) == None:
                self.setSettleCalls += 1
                return True
        elif spot[0] == 11 and self.getSettlement((spot[0] - 1, spot[1])) == None and self.getSettlement((spot[0]- 1, spot[1] + 1)) == None:
            self.setSettleCalls += 1
            return True
        else:
            if self.getSettlement((spot[0] + 1, spot[1])) == None and self.getSettlement((spot[0] - 1, spot[1])) == None and self.getSettlement((spot[0] - 1, spot[1] -1)) == None:
                self.setSettleCalls += 1
                return True
        return False


    def setSettlement(self, controller, player, spot, settType):
        spot = (spot[1], spot[0])

        if spot[0] in [0,11]:
            spot = (spot[0], int(((spot[1] - 1)/2) - 1))
        elif spot[0] in [1,2,9,10]:
            spot = (spot[0], int((spot[1]/2) - 1))
        elif spot[0] in [3,4,7,8]:
            spot = (spot[0], int((spot[1] - 1)/2))
        else:
            spot = (spot[0], int(spot[1]/2))

        if self.isSpotValid(spot) == False or (self.getSettlement((spot[0], spot[1])) != None and settType == 1):
            return False
        
        if self.validSettlement(spot, player, controller) == False:
            return False

        if(settType == 1):
            #Check if player already has settlement there and return False if they do
            for players in controller:
                if spot in players.settlementSpots or players.citySpots:
                    return False

            player.settlementQuantity -= 1

            self.settleSpots[spot[0]][spot[1]] = player.name + "'s " + 'Settlement'
            player.settlementSpots.append(spot)

            for key in self.settleOnTile:
                if spot in self.settleOnTile[key]:
                    insertSpot = self.settleOnTile[key].index(spot)
                    self.settleOnTile[key].insert(insertSpot, player.name + "'s " + 'Settlement')
            image = np.array(Image.open("images/test.png"))
            draw.drawSettle(image, player, spot)

        else:
            print("GOT HERE")
            #Check if player has there own settlement there return False if they don't and can't upgrade to city or return False if anyone already has a city there
            for players in controller:
                if spot in players.citySpots or spot not in player.settlementSpots:
                    print("City not allowed")
                    return False

            player.cityQuantity -= 1 

            self.settleSpots[spot[0]][spot[1]] = player.name + "'s " + 'City'
            player.citySpots.append(spot)

            for key in self.settleOnTile:
                if spot in self.settleOnTile[key]:
                    insertSpot = self.settleOnTile[key].index(spot)
                    self.settleOnTile[key].insert(insertSpot, player.name + "'s " + 'City')
            image = np.array(Image.open("images/test.png"))
            draw.drawCity(image, player, spot)
            
        player.victoryPoints += 1
        return True

    def getSettlement(self, spot):
        try:
            return self.settleSpots[spot[0]][spot[1]]
        except:
            return None

    def getMaterial(self, controller, num):
        materialAndPoints = {}
        for material in self.materialNumberTile[num]:
            for key in self.settleOnTile:
                if material == key and f"({self.robberLocation[0]},{self.robberLocation[1]})" not in str(material):
                    materialAndPoints[material] = self.settleOnTile[material]

        for material in materialAndPoints:
            for player in controller:
                toBeGiven = materialAndPoints[material].count(player.name + "'s Settlement") + materialAndPoints[material].count(player.name + "'s City") * 2

                if('rock' in material):
                    player.currentResources['rock'] += toBeGiven
                if('brick' in material):
                    player.currentResources['brick'] += toBeGiven
                if('wheat' in material):
                    player.currentResources['wheat'] += toBeGiven
                if('tree' in material):
                    player.currentResources['wood'] += toBeGiven
                if('sheep' in material):
                    player.currentResources['sheep'] += toBeGiven
               
    #postType one of ["Wheat", "Rock", "Brick", "Wood", "Sheep", "3for1", "4for1"]
    def postAccess(self, player, postType):
        if postType == "4for1":
            return True

        for value in self.portsSettleSpots[postType]:
            if value in player.settlementSpots:
                return True
        return False

    def moveRobber(self, newLocation):
        newLocation = (newLocation[1], newLocation[0])

        if newLocation[0] in [1.5, 9.5]:
            if newLocation[0] == 1.5:
                newLocation = (0, int(((newLocation[1] - 1)/2) - 1))
            else: newLocation = (4, int(((newLocation[1] - 1)/2) - 1))

        elif newLocation[0] in [3.5, 7.5]:
            if newLocation[0] == 3.5:
                newLocation = (1, int((newLocation[1]/2) - 1))
            else: newLocation = (3, int((newLocation[1]/2) - 1))

        elif newLocation[0] == 5.5:
            newLocation = (2, int((newLocation[1] - 1)/2))
        else: return False

        self.robberLocation = newLocation
        image = np.array(Image.open("images/test.png"))
        draw.drawRobber(self, image)
