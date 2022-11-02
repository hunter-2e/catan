import cv2
import numpy as np

photo  = "C:\\Users\\hunter\\Documents\\Python Scripts\\catan\\gui\\build\\background.png"

image = cv2.imread(photo)

window_name = 'Drawing Board'

topLeft = [225,70]
botLeft = [225, 160]
bot = [310, 210]
botRight = [400, 160]
topRight = [400, 70]
top = [310, 20]

allVertex = [topLeft, botLeft, bot, botRight, topRight, top]

isClosed = True
color = (255, 0, 0)
thickness = 2


for tile in range(19):
    if tile not in [3,7,12,16]:
        pts = np.array([topLeft, botLeft,
                    bot, botRight,
                        topRight, top],
                    np.int32)
        color = (0,255,0)
    else:
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
        color = (0,0,255)
    pts = np.array([topLeft, botLeft,
                    bot, botRight,
                        topRight, top],
                    np.int32)   
    pts = pts.reshape((-1, 1, 2))

    cv2.fillPoly(image, [pts], color)
    image = cv2.polylines(image, [pts], isClosed, (0,0,0), thickness)
    

    for vertex in allVertex:
            vertex[0] += 175
    


# Displaying the image
while(1):
     
    cv2.imshow(window_name, image)
    cv2.imwrite('test.png', image)
    if cv2.waitKey(20) & 0xFF == 27:
        break
         
cv2.destroyAllWindows()