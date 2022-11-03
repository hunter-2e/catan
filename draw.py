import cv2
import numpy as np
import itertools, string

photo  = "background.png"

path = cv2.imread(photo)

topLeft = [225,90]
botLeft = [225, 180]
bot = [310, 230]
botRight = [400, 180]
topRight = [400, 90]
top = [310, 40]

allVertex = [topLeft, botLeft, bot, botRight, topRight, top]

isClosed = True
color = (255, 0, 0)
thickness = 2


def drawBoard(board, image):
    startingTile = [0,0]
    tileNumbers = board.materialNumberTile
    tileColors = list(itertools.chain.from_iterable(board.tileSpots))

    print(tileNumbers)
    for tile in range(19):
        for number in tileNumbers:
            for material in tileNumbers[number]:
                if '('+ str(startingTile[0]) + ',' + str(startingTile[1]) + ')' in material:
                    numToDraw = number
                    break
                   
        if tile not in [2,6,11,15]:
            startingTile[1] += 1
        else:
            startingTile[1] = 0
            startingTile[0] += 1

        if tile in [3,7,12,16]:
            for vertex in allVertex:
                vertex[1] += 140
                if tile == 3:
                    vertex[0] -= 612.5
                elif tile == 7:
                    vertex[0] -= 787.5
                elif tile == 12:
                    vertex[0] -= 787.5
                else:
                    vertex[0] -= 612.5

        pts = np.array([topLeft, botLeft,
                        bot, botRight,
                            topRight, top],
                        np.int32)   
        pts = pts.reshape((-1, 1, 2))

        if tileColors[tile] == 'rockTile':
            color = (99, 115, 120)
        elif tileColors[tile] == 'brickTile':
            color = (28, 104, 166)
        elif tileColors[tile] == 'sheepTile':
            color = (48, 161, 82)
        elif tileColors[tile] == 'wheatTile':
            color = (121, 231, 230)
        elif tileColors[tile] == 'treeTile':
            color = (17, 63, 84)
        else:
            color = (44, 7,166)

        cv2.fillPoly(image, [pts], color)
        image = cv2.circle(image, (int(top[0]), top[1] + 95), 30, (0,0,0), -1)
        if(numToDraw > 9):
            image = cv2.putText(image, str(numToDraw), (int(top[0] - 20), top[1] + 105), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
        else: image = cv2.putText(image, str(numToDraw), (int(top[0] - 10), top[1] + 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
        image = cv2.polylines(image, [pts], isClosed, (0,0,0), thickness)
        

        for vertex in allVertex:
                vertex[0] += 175
        drawGrid(image)
    cv2.imwrite('test.png', image)

def drawGrid(image):
    capitalLetters = list(string.ascii_uppercase)
    letterIndex = 0
    xCoord = 50
    yCoord = 50

    for num in range(11):
        image = cv2.putText(image, capitalLetters[letterIndex], (xCoord, 23), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 1)
        letterIndex += 1
        xCoord += 85
    
    for num in range(12):
        image = cv2.putText(image, str(num), (0, yCoord), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 1)
        if(num % 2 == 0):
            yCoord += 50
        else: yCoord += 90

def getSpot(spot):
    spotAdj = [spot[1],spot[0]]

    firstSpot = [310, 40]
    if spot[0] == 1:
        firstSpot[1] += 50
        firstSpot[0] -= 85
    elif spot[0] == 2:
        firstSpot[1] += 140
        firstSpot[0] -= 85
    elif spot[0] == 3:
        firstSpot[1] += 190
        firstSpot[0] -= 175
    elif spot[0] == 4:
        firstSpot[1] += 280
        firstSpot[0] -= 175
    elif spot[0] == 5:
        firstSpot[1] += 330
        firstSpot[0] -= 260
    elif spot[0] == 6:
        firstSpot[1] += 420
        firstSpot[0] -= 260
    elif spot[0] == 7:
        firstSpot[1] += 470
        firstSpot[0] -= 175
    elif spot[0] == 8:
        firstSpot[1] += 560
        firstSpot[0] -= 175
    elif spot[0] == 9:
        firstSpot[1] += 610
        firstSpot[0] -= 85
    elif spot[0] == 10:
        firstSpot[1] += 700
        firstSpot[0] -= 85
    elif spot[0] == 11: 
        firstSpot[1] += 750
        
    firstSpot[0] += spotAdj[0] * 175

    return firstSpot

def determineColor(player):

    color = player.color

    if(color == "blue"):
        color = (255,0,0)
    elif(color == "red"):
        color = (0,0,255)
    elif(color == "orange"):
        color = (27, 133, 241)
    elif(color == "white"):
        color = (255,255,255)

    return color

def drawSettle(image, player, spot):

    boardLocation = getSpot(spot)
    settleColor = determineColor(player)
    
    cv2.rectangle(image,(boardLocation[0] - 15,boardLocation[1]-15),(boardLocation[0] + 15,boardLocation[1] + 15),settleColor,-1)
    cv2.imwrite('test.png', image)

def drawCity(image, player, spot):

    boardLocation = getSpot(spot)
    settleColor = (255,255,255)
    
    cv2.rectangle(image,(boardLocation[0] - 10,boardLocation[1]-10),(boardLocation[0] + 10,boardLocation[1] + 10),settleColor,-1)
    cv2.imwrite('test.png', image)

def drawRoad(image, player, spot1, spot2):
    
    boardLocation1 = getSpot(spot1)
    boardLocation2 = getSpot(spot2)

    roadColor = determineColor(player)

    cv2.line(image, boardLocation1, boardLocation2, roadColor, 4) 
    cv2.imwrite('test.png', image)








# Displaying the image
img = cv2.cvtColor(path, cv2.COLOR_BGR2RGB)

