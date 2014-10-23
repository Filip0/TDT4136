from math import exp
from random import random, shuffle, randint
import numpy as np
import Image
import ImageDraw
import ImageFont
class SimulatedAnnealing(object):
    """docstring for ClassName"""
    tMax = 100.0
    t = 100.0
    dT = 0.1
    board = None
    fTarget = 1.0
    n = 0
    m = 0
    k = 0


    def __init__(self, board,m,n,k):
        super(SimulatedAnnealing, self).__init__()
        self.board = board
        self.n = n
        self.m = m
        self.k = k 


    def run(self):
        # Set start variable as the F(P_start) and P_start
        start = (self.objective(self.board), self.board)
        # Set current to start
        current = start
        # While
        while self.t > 0:
            if current[0] >= self.fTarget:
                return current
            neighbors = self.neighbors(current)
            nMax = (0,None)
            for n in neighbors:
                nTemp = self.objective(n)
                if nTemp > nMax[0]: nMax = (nTemp,n)
            q = (nMax[0]-current[0])/current[0]
            print "Q: " + str(q)
            print "T: " + str(self.t)
            print "EXP: " + str(exp(-q/self.t))
            p = min(1, exp(-q/self.t))
            x = random()
            if x > p:
                current = nMax
            self.t -= self.dT
            #raw_input("Enter:")
        return current


    def objective(self,p):
        score = 1.0
        maxEgg = self.k*len(p)
        sums = sum(sum(p,[]))
        if sums > maxEgg: score -= 0.1
        for row in p:
            rowsum = sum(row)
            if rowsum > self.k: score -= 0.1#*(rowsum-self.k)
        for i in xrange(self.n):
            colsum = sum(a[i] for a in p)
            if rowsum > self.k: score -= 0.1#*(colsum-self.k)
        a = np.array(p)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
        for diag in diags:
            diagsum = sum(diag)
            if diagsum > self.k: score -= 0.1#*(diagsum-self.k)

        print "Score: " + str(score)
        print "Sums/maxEgg: " + str(sums/maxEgg)
        return max(0.1, (sums/maxEgg)-score)


    def neighbors(self, current):
        boards = []
        for i in xrange(5):
            copy = current[1]
            r1,r2 = randint(0,self.m-1),randint(0,self.n-1)
            r2,r3 = randint(0,self.m-1),randint(0,self.n-1)
            print r1,r2
            if copy[r1][r2] == 1:
                copy[r1][r2] = 0
            else:   
                copy[r1][r2] = 1
            boards.append(copy)
        return boards

def draw(board, n, m):
    img = Image.new( 'RGB', (n*20,m*20), "white")
    # Craete ImageDraw
    idraw = ImageDraw.Draw(img)

    for y in range(0,m):
        for x in range(0,n):
            if board[y][x] == 0:
                c = (255,255,255)
            else:
                c = (73,216,245)

            idraw.rectangle([(x*20,y*20),(x*20+20,y*20+20)], fill=c, outline=(0,0,0))
    img.save("test.png","PNG")


def main():
    #t = raw_input("M N K: ")
    #t = t.split()
    #m = int(t[0]) # Rows
    #n = int(t[1]) # Columns
    #k = int(t[2]) # Max number of eggs per row, column, and diagonal
    m,n,k = 5,5,2
    board = [[0 for x in xrange(n)] for x in xrange(m)]
    for row in board:
        for i in xrange(k):
            row[i] = 1
        shuffle(row) 
    for row in board:
        print row
    print sum(sum(board,[]))
    sa = SimulatedAnnealing(board,m,n,k)
    result = sa.run()
    for row in result:
        print row
    draw(result[1],m,n)

if __name__ == "__main__":
    main()