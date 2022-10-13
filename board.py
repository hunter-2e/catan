import random
import this
import player as ply

class Board:
    def __init__(self):
        #Places a settlement can be built
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
          [(9,1),(10,0),(10,1),(11,0),(11,1),(12,0)],
          [(9,2),(10,1),(10,2),(11,1),(11,2),(12,1)],
          [(9,3),(10,2),(10,3),(11,2),(11,3),(12,2)]]

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
        for row in self.tileSpots:
            yTile = 0
            zPoints = 0
            for tile in range(len(row)):
                 chosenTile = random.choice([tilesLeft for tilesLeft in self.tilesAvailable.keys() if self.tilesAvailable[tilesLeft] > 0])
                 
                 if chosenTile == 'robberTile':
                    chosenNum = 7
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


    def setRoad(self, spot1, spot2):
        self.roadsPlaced.append([spot1,spot2])



    def getRoad(self, spot1, spot2):
        if([spot1, spot2] in self.roadsPlaced):
            return True
        else: return False



    def setSettlement(self, player, spot, settType):
        if(self.settleSpots[spot[0]][spot[1]] != None):
            return "This space already has a settlement."
        else:
            player.settlementQuantity -= 1
            if(settType == 1):
                self.settleSpots[spot[0]][spot[1]] = player.name + "'s " + 'Settlement '
            else: self.settleSpots[spot[0]][spot[1]] = player.name + "'s " + 'City'



    def getSettlement(self, spot):
        return self.settleSpots[spot[0]][spot[1]]



    def getMaterial(self, num):
        materialAndPoints = {}
        for material in self.materialNumberTile[num]:
            for key in self.settleOnTile:
                if material == key:
                    materialAndPoints[material] = self.settleOnTile[material]
        return materialAndPoints

    def postAccess():
        return 1

Hunter = ply.Player("Hunter", 1)
board = Board()
board.setSettlement(Hunter, (0,0), 2)
print(board.getSettlement((0,0)))

print(board.getMaterial(5))