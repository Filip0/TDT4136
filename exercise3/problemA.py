from heapq import heappush, heappop
import math
import fileinput
import Image
import ImageDraw

class node:
    xPos = 0
    yPos = 0
    g = 0
    h = 0
    f = 0
    status = False
    parent = None
    kids = []

    def __init__(self,x,y,parent):
        self.xPos = x
        self.yPos = y
        self.parent = parent

    def manhattan(self,endNode):
        # Manhattan distance |x1 - x2| + |y1 - y2|
        xD = self.xPos - endNode.xPos
        yD = self.yPos - endNode.yPos

        return abs(xD) + abs(yD)

    def __cmp__(self, other):
        if other == None: return False
        return cmp(self.f, other.f)

    def __eq__(self, other):
        if other == None: return False
        return self.xPos == other.xPos and self.yPos == other.yPos
    
    def __str__(self):
        return "Node: x: " + str(self.xPos) + " y: " + str(self.yPos) 

    def __repr__(self):
        return str(self)

class Astar:

    Open, Closed = [], []
    graph = []
    start = None
    end = None
    x = 0
    y = 0

    def __init__(self, start,end,graph):
        self.Open.append(start)
        self.start = start
        self.end = end
        self.graph = graph
        self.x = len(graph[0])
        self.y = len(graph)

    def pathfinder(self):
        o,c = [self.start] , []

        while o:
            x = heappop(o)
            if x in c: continue
            heappush(c,x)
            if x == self.end: return x,True
            n = self.neighbors(x)
            print len(n)
            for v in n:
                print "Any neighbors?"
                if v in c: continue
                g = x.g + 1
                if v not in o or g < o[o.index(v)].g:
                    print "Neighbor not in Open list or g() less than existing"
                    v.g = g
                    v.h = v.manhattan(self.end)
                    v.f = g + v.h
                    if v not in o:
                        print "Adding neighbor to open list"
                        heappush(o,v)

        return None, False


    def neighbors(self,current):
        neighbors = []
        x =current.xPos
        y = current.yPos
        array = [(x-1,y),(x+1,y),(x,y+1),(x,y-1)]
        for x_ in range(max(0,current.xPos-1),min(self.x,current.xPos+2)):
            for y_ in range(max(0,current.yPos-1),min(self.y,current.yPos+2)):
                if (current.xPos,current.yPos)==(x_,y_): continue
                if self.graph[y_][x_] == '#': continue
                neighbors.append(node(x_,y_,current))
        return neighbors

    def reconstruct_path(self,current):
        path = [(current.xPos,current.yPos)]

        while current.parent:
            print len(path)
            path.append((current.parent.xPos,current.parent.yPos))
            current = current.parent
        return path

def drawImage(graph, path):
    img = Image.new( 'RGB', (len(graph[0])*10,len(graph)*10), "white") # create a new black image
    idraw = ImageDraw.Draw(img)
    print "_-------"
    print len(graph[0])
    print len(graph)
    for y in range(0,len(graph)):
        for x in range(0,len(graph[0])):
            #graph[y][x]
            c = color(graph[y][x])
            idraw.rectangle([(x*10,y*10),(x*10+10,y*10+10)], fill=c, outline=(0,0,0))
            if (x,y) in path:
                c = (107,97,255)
                idraw.rectangle([(x*10+3,y*10+3),(x*10+7,y*10+7)], fill=c, outline=(0,0,0))
            
    img.save("img1.png","PNG")

def color(x):
    return {
        '.': (255,255,255),
        '#': (114,114,114),
        'A': (90,180,90),
        'B': (255,90,90),
        }.get(x, (0,0,0))
def main():
    q = []
    for line in fileinput.input():
        l = list(line)
        l.pop()
        if 'A' in l:
            print l.index('A')
            print len(q)
            startNode =node(l.index('A'),(len(q)),None)
        if 'B' in l:
            print l.index('B')
            print len(q)
            endNode = node(l.index('B'),(len(q)),None)

        q.append(l)
    astar = Astar(startNode,endNode,q)
    current, b = astar.pathfinder()
 
    
    path = astar.reconstruct_path(current)
    print path
    drawImage(q,path)


if __name__ == "__main__":
    main()