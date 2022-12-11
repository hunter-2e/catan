from collections import deque
import itertools

# this is an example list of coordinate touples, 
# this should be how you structure the input of the singlePlayerLongestRoad function
# i have to test if this works with the following: https://boardgames.stackexchange.com/questions/15526/in-catan-can-you-continue-a-circular-road


Emanuel = [((0,0),(1,1)),   # Cycle with two protrusions, it should return 7 and does
           ((1,1),(2,1)),   #
           ((2,1),(3,1)),   #    / \
           ((3,1),(2,0)),   #   |   |      
           ((2,0),(1,0)),   #  / \ / \
           ((1,0),(0,0)), 
           ((2,0),(3,0)),
           ((2,1),(3,2)),
           ]
           
Kobi =    [((0,0),(1,1)),   # Random Lines No Cycles, it should return 8 and does
           ((3,2),(4,2)),   #           
           ((1,1),(2,1)),   # \ / \
           ((1,1),(0,1)),   #  |   |
           ((0,1),(1,2)),   #     / \ /
           ((2,2),(1,2)),   #    |
           ((2,2),(3,3)),   #     \
           ((3,3),(2,3)),   #      |
           ((3,2),(2,2)),
           ((5,3),(6,3)),
           ((4,2),(5,3)),
           ]

Chamin =  [((0,0),(1,1)),   # Two Cycles, it should return 11, and does
           ((5,1),(4,1)),   #           
           ((2,1),(3,1)),   #    / \ 
           ((3,1),(2,0)),   #   |   |      
           ((2,0),(1,0)),   #  / \ /
           ((1,0),(0,0)),   # |   |
           ((2,0),(3,0)),   #  \ /
           ((3,0),(4,0)), 
           ((4,0),(5,1)), 
           ((3,1),(4,1)),
           ((1,1),(2,1)),
           ]

Chamin2 = [((0,0),(1,1)),   # Two Cycles, it should return 14, and does 
           ((1,1),(2,1)),   #           
           ((3,1),(2,1)),   #    / \ 
           ((2,0),(3,1)),   #   |   |      
           ((2,0),(1,0)),   #    \ / \
           ((1,0),(0,0)),   #         |      
           ((2,1),(3,2)),   #        / \
           ((3,2),(4,2)),   #       |   |
           ((5,2),(4,2)),   #        \ /
           ((4,2),(5,3)),
           ((5,2),(6,2)),
           ((6,2),(7,2)),   
           ((7,2),(6,3)),
           ((5,3),(6,3)),
           ]

Chamin3 =  [((0,0),(1,1)),  # Two Cycles with one protrusion, it should return 11, but returns 12, whyyyyyy?????
           ((5,1),(4,1)),   #           
           ((2,1),(3,1)),   #    / \ / 
           ((3,1),(2,0)),   #   |   |      
           ((2,0),(1,0)),   #  / \ /
           ((1,0),(0,0)),   # |   |
           ((2,0),(3,0)),   #  \ /
           ((3,0),(4,0)), 
           ((4,0),(5,1)), 
           ((3,1),(4,1)),
           ((1,1),(2,1)),
           ((1,1),(0,1)),
           ]

Hunter =  [((0,0),(1,1)),   # Three cycles, it should return 14, and does
           ((1,1),(2,1)),   #
           ((5,1),(4,1)),   #           
           ((2,1),(3,1)),   #    / \
           ((3,1),(2,0)),   #   |   |      
           ((2,0),(1,0)),   #  / \ / \
           ((1,0),(0,0)),   # |   |   |
           ((2,0),(3,0)),   #  \ / \ /
           ((3,0),(4,0)), 
           ]

Hunter2 = [((0,0),(1,1)),   # Two cycles, it should return 14, and does
           ((1,1),(2,1)),   # 
           ((5,1),(4,1)),   #           
           ((2,1),(3,1)),   #    / \
           ((3,1),(2,0)),   #   |   |      
           ((2,0),(1,0)),   #  / \ / \
           ((1,0),(0,0)),   # |       |
           ((2,0),(3,0)),   #  \ / \ /
           ((3,0),(4,0)), 
           ((4,0),(5,1)),         
           ((4,1),(5,2)),
           ((5,2),(4,2)),
           ((4,2),(3,2)),
           ((3,2),(2,1)),
           ]

# https://www.geeksforgeeks.org/longest-path-undirected-tree/
# graph class inspired by this link
class Graph:

    def __init__(self, vertices):
        self.vertices = vertices
        self.adj = {i: [] for i in range(self.vertices)}
 
    def addEdge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
 
    def BFS(self, u):
        visited = [False for i in range(self.vertices + 1)]
        distance = [-1 for i in range(self.vertices + 1)]
        distance[u] = 0
        queue = deque()
        queue.append(u)
        visited[u] = True
 
        while queue:
            front = queue.popleft()
            for i in self.adj[front]:
                if not visited[i]:
                    visited[i] = True
                    distance[i] = distance[front]+1
                    queue.append(i)
 
        maxDis = 0
 
        for i in range(self.vertices):
            if distance[i] > maxDis:
                maxDis = distance[i]
                nodeIdx = i
 
        return nodeIdx, maxDis

    def LongestPathLength(self):
        node, Dis = self.BFS(0)
        node_2, LongDis = self.BFS(node)
        return int(LongDis)
 
 # this is the function that prints longest road. 
 # It's a quick modification to get it to return longest road if that's how you want to structure it

def outerLongestRoad(playerCoords, players, playerChecked):

    disruptingSettles = []

    for player in players:
        if player != playerChecked:
            for settle in player.settlementSpots:
                disruptingSettles.append(settle)
    
    for connectingRoads in playerCoords:
        for road in connectingRoads:
            if road in disruptingSettles:
                playerCoords.remove(connectingRoads)
 
    longestRoadNoRemoval = 0
    longestRoadOneRemoval = 0
    longestRoadTwoRemoval = 0
    longestRoadThreeRemoval = 0

    def innerLongestRoad(playerCoords):

        uniqueIndicies = []
        uniqueCoords   = []
        for coordPair in playerCoords:
            for coord in coordPair:
                uniqueCoords.append(coord)
        
        # all unique coordinates from list of a player's roads
        uniqueCoords = list(sorted(set(uniqueCoords)))

        i = 0
        while i < len(uniqueCoords):
            uniqueIndicies.append(i)
            i += 1

        coordsAsDict = dict(zip(uniqueCoords, uniqueIndicies))
        
        G = Graph(len(coordsAsDict))
        for coordPair in playerCoords:
            G.addEdge(int(coordsAsDict[coordPair[0]]), int(coordsAsDict[coordPair[1]]))

        return G.LongestPathLength()
    
    # code for finding the value of longestRoadNoRemoval
    if (innerLongestRoad(playerCoords) > longestRoadNoRemoval):
        longestRoadNoRemoval = innerLongestRoad(playerCoords)

    # code for finding the value of longestRoadOneRemoval
    if (len(playerCoords) >= 6):
        OneRemovalTemp = playerCoords

        for i in OneRemovalTemp:
            temp = OneRemovalTemp.pop(0)

            if (innerLongestRoad(OneRemovalTemp) > longestRoadOneRemoval):
                longestRoadOneRemoval = innerLongestRoad(OneRemovalTemp)

            OneRemovalTemp.append(temp)

        # code for finding the value of longestRoadTwoRemoval
        TwoRemovalTemp = itertools.combinations(playerCoords, len(playerCoords) - 2)

        for i in TwoRemovalTemp:
            if (innerLongestRoad(i) > longestRoadTwoRemoval):
                longestRoadTwoRemoval = innerLongestRoad(i)

        # code for finding the value of longestRoadThreeRemoval
        ThreeRemovalTemp = itertools.combinations(playerCoords, len(playerCoords) - 3)

        for i in ThreeRemovalTemp:
            if (innerLongestRoad(i) > longestRoadThreeRemoval):
                longestRoadThreeRemoval = innerLongestRoad(i)

    print(longestRoadNoRemoval)
    print(longestRoadOneRemoval)
    print(longestRoadTwoRemoval)
    print(longestRoadThreeRemoval)

    if (longestRoadNoRemoval >= longestRoadOneRemoval)   and (longestRoadNoRemoval >= longestRoadTwoRemoval)  and (longestRoadNoRemoval >= longestRoadThreeRemoval) :
        print("1st if: ")
        return longestRoadNoRemoval 
    elif (longestRoadOneRemoval >= longestRoadNoRemoval) and (longestRoadOneRemoval >= longestRoadTwoRemoval) and (longestRoadOneRemoval >= longestRoadThreeRemoval):
        print("2nd if: ")
        return longestRoadOneRemoval + 1
    elif (longestRoadTwoRemoval >= longestRoadNoRemoval) and (longestRoadTwoRemoval >= longestRoadOneRemoval) and (longestRoadTwoRemoval >= longestRoadThreeRemoval):
        print("3rd if: ")
        return longestRoadTwoRemoval + 2
    else:
        print("4th if: ")
        return longestRoadThreeRemoval + 2
    


# testing with the different shapes displayed above:
# Note that longest road interuption by other players has not been implemented yet
# print("Emanuel : " + str(outerLongestRoad(Emanuel)) + "\n")
# print("Kobi    : " + str(outerLongestRoad(Kobi)) + "\n")
# print("Chamin  : " + str(outerLongestRoad(Chamin)) + "\n")
# print("Chamin2 : " + str(outerLongestRoad(Chamin2)) + "\n")
# print("Chamin3 : " + str(outerLongestRoad(Chamin3)) + "\n")
# print("Hunter  : " + str(outerLongestRoad(Hunter)) + "\n")