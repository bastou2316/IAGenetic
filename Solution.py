from math import pow, sqrt

class Solution:
	def __init__(self, townsList):
		self.townsList = []
		for t in townsList:
			self.townsList.append(t)
		self.distancesSum = self.checkPathDistance()

	def checkPathDistance(self):
		sum = 0
		for x in range(len(self.townsList)-1):
			city1 = self.townsList[x]
			city2 = self.townsList[x + 1]
			sum += (self.euclidianDistanceBetweenTwoTowns(city1, city2))
		return sum

	def euclidianDistanceBetweenTwoTowns(self, a, b):
		return float(sqrt(pow((int(a.x) - int(b.x)), 2) + pow((int(a.y) - int(b.y)), 2)))

	def getDistancesSum(self):
		return self.distancesSum
	
	def cross():
		return 0

	def mutate():
		return 0