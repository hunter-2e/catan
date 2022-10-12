import random

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

        self.materialNumberTile = {}

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
            'ten': 2,
            'eight': 2,
            'six': 2,
            'two': 1,
            'twelve': 1,
            'eleven': 2,
            'nine': 2,
            'three': 2,
            'four': 2,
            'five': 2,
            'seven': 1
        }


        #Populating tileSpots randomly with available material types and a number
        for row in self.tileSpots:
            for tile in range(len(row)):
                 chosenTile = random.choice([tilesLeft for tilesLeft in self.tilesAvailable.keys() if self.tilesAvailable[tilesLeft] > 0])
                 
                 if chosenTile == 'robberTile':
                    chosenNum = 'seven'
                 else:
                    chosenNum = random.choice([numLeft for numLeft in self.numbersAvailable.keys() if self.numbersAvailable[numLeft] > 0 and numLeft != 'seven'])

                 try:
                    if(self.materialNumberTile[chosenNum] is None): 
                        self.materialNumberTile[chosenNum] = [chosenTile]
                    else: 
                        self.materialNumberTile[chosenNum].append([chosenTile])
                 except:
                        self.materialNumberTile[chosenNum] = [chosenTile]

                 row[tile] = chosenTile

                 self.tilesAvailable[chosenTile] -= 1
                 self.numbersAvailable[chosenNum] -= 1

        print(self.materialNumberTile)

GAME = Board()