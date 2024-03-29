from heapq import heappush, heappop
import math
import fileinput
import Image
import ImageDraw

class Node:
    xPos = 0
    yPos = 0
    g = 0               # Cost
    h = 0               # Heuristic cost
    f = 0               # Sum of g and h
    parent = None       # Parent node

    # Object constructor
    def __init__(self,x,y,parent):
        self.xPos = x
        self.yPos = y
        self.parent = parent

    # Calculates h values by using manhattan distance
    def manhattan(self,endNode):
        # Manhattan distance |x1 - x2| + |y1 - y2|
        xD = self.xPos - endNode.xPos
        yD = self.yPos - endNode.yPos

        return abs(xD) + abs(yD)

    # Override default compare, and compare the nodes on their f values
    def __cmp__(self, other):
        if other == None: return False
        return cmp(self.f, other.f)

    # Override default equality checks, and check position equality
    def __eq__(self, other):
        if other == None: return False
        return self.xPos == other.xPos and self.yPos == other.yPos
    
    # return value when printed
    def __str__(self):
        return "Node: x: " + str(self.xPos) + " y: " + str(self.yPos) 

    def __repr__(self):
        return str(self)

class Astar:

    graph = []                      # The initial graph
    start = None                    # The start node
    end = None                      # The end node
    x = 0                           # The x length of the graph
    y = 0                           # The y length of the graph

    # A* Class constructor
    def __init__(self, start,end,graph):
        self.start = start     
        self.end = end
        self.graph = graph
        self.x = len(graph[0])
        self.y = len(graph)

    # Method for finding the paths
    def pathfinder(self):

        # Creation of the open and closed lists, add startnode to open list
        o,c = [self.start] , []

        while o:                                            # WHile there are items in the open list
            x = heappop(o)                                  # Pop the best item from open list
            if x in c: continue                             # If node is in the closed list, continue
            heappush(c,x)                                   # Push the node to the closed list
            if x == self.end: return x,True                 # If node is end node, return
            n = self.neighbors(x)                           # Find neighbors
            for v in n:                                     # Itterate neigbors
                if v in c: continue                         # If neighbor is in closed list, continue 
                g = x.g + 1                                 # Calculate g for neighbor 
                if v not in o or g < o[o.index(v)].g:       # If not in open list or v has better cost from this node
                    v.g = g                                 
                    v.h = v.manhattan(self.end)
                    v.f = g + v.h
                    if v not in o:                          # If not in open list, 
                        heappush(o,v)

        return None, False                                  # Did not find a path, return


    def neighbors(self,current):
        # FInd all neighbors
        neighbors = []
        x = current.xPos
        y = current.yPos
        # Array to search North, South, West, and East
        array = [(x-1,y),(x+1,y),(x,y+1),(x,y-1)]
        for x_,y_ in array:
            # Make sure it is not out of bounds
            if 0 <= x_ <= self.x-1 and 0 <= y_ <= self.y-1:
                # Ignore walls
                if self.graph[y_][x_] == '#': continue
                # Append to neighbors list 
                neighbors.append(Node(x_,y_,current))  
        # Return neighbors
        return neighbors

    def reconstruct_path(self,current):
        # Reconstruct path from the current node
        path = [(current.xPos,current.yPos)]

        # While current has a parent, add the parent and change current to parent
        while current.parent:
            path.append((current.parent.xPos,current.parent.yPos))
            current = current.parent
        # When there is no parent we are back at the start node.
        return path

def drawImage(graph, path):
    # Create new image with 20x20 px for each node
    img = Image.new( 'RGB', (len(graph[0])*20,len(graph)*20), "white")
    # Craete ImageDraw
    idraw = ImageDraw.Draw(img)
    # Itterate over all nodes
    for y in range(0,len(graph)):
        for x in range(0,len(graph[0])):
            # Get correct color            
            c = color(graph[y][x])
            # Draw rectangle 20x20 with color
            idraw.rectangle([(x*20,y*20),(x*20+20,y*20+20)], fill=c, outline=(0,0,0))
            # If path, draw a dot
            if (x,y) in path:
                c = (107,97,255)
                idraw.rectangle([(x*20+6,y*20+6),(x*20+14,y*20+14)], fill=c, outline=(0,0,0))
            
    img.save("test.png","PNG")

def color(x):
    return {
        '.': (255,255,255),
        '#': (114,114,114),
        'A': (90,180,90),
        'B': (255,90,90),
        }.get(x, (0,0,0))

def main():
    q = []                                                 # Main graph
    for line in fileinput.input():                         # File input 
        l = list(line)                                     # Convert string to list
        l.pop()                                            # Pop the \n newline from the list
        if 'A' in l:                                       # If A aka the start point
            startNode =Node(l.index('A'),(len(q)),None)    # Create startnode
        if 'B' in l:                                       # If B aka the end point
            endNode = Node(l.index('B'),(len(q)),None)     # Create endnode

        q.append(l)                                        # Append list to graph
    astar = Astar(startNode,endNode,q)                     # Create Astar object
    current, b = astar.pathfinder()                        # Run pathfinder
    path = astar.reconstruct_path(current)                 # Reconstruct path
    drawImage(q,path)                                      # DrawImage


if __name__ == "__main__":
    main()