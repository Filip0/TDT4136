from math import exp
from random import random
class SimulatedAnnealing(object):
	"""docstring for ClassName"""
	tMax = 10
	t = 10
	dT = 0.1
	board = None
	fTarget = 1


	def __init__(self, board):
		super(ClassName, self).__init__()
		self.t = tMax
		self.board = board


	def run(self):
		# Set start variable as the F(P_start) and P_start
		start = (objective(self.board), self.board)
		# Set current to start
		current = start
		# While
		while t > 0:
			return self.board if fCurrent >= self.fTarget else continue
			neighbors = neighbors()
			nMax = (0,None)
			for n in neighbors:
				nTemp = objective(n)
				if nTemp > nMax[0]: nMax = (nTemp,n)
			q = (nMax[0]-current[0])/current[0]
			p = min(1, exp(-q/self.t))
			x = random()
			if x > p:
				current = nMax
			t = t-dt
		return current


	def objective(self,p):
		pass

	def neighbors():
		pass