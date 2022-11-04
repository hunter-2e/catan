from collections import deque

Emanuel = [((0,1),(1,1)), ((2,2),(2,1)), ((1,2),(2,2)),((2,1),(3,1)), ((1,1),(1,2)), ((3,1),(4,1)), ((3,1),(3,2)), ((3,2),(3,3)), ((3,3),(4,3)) ]

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
        print("This player's longest road is " + str(LongDis) + " road(s)")
 
 
def singlePlayerLongestRoad(playerCoords):

    uniqueIndicies = []
    uniqueCoords   = []
    for coordPair in playerCoords:
        for coord in coordPair:
            uniqueCoords.append(coord)
    
    uniqueCoords = list(sorted(set(uniqueCoords)))

    i = 0
    while i < len(uniqueCoords):
        uniqueIndicies.append(i)
        i += 1

    coordsAsDict = dict(zip(uniqueCoords, uniqueIndicies))
    
    G = Graph(len(coordsAsDict))
    for coordPair in playerCoords:
        G.addEdge(int(coordsAsDict[coordPair[0]]), int(coordsAsDict[coordPair[1]]))

    G.LongestPathLength()

singlePlayerLongestRoad(Emanuel)
