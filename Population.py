from random import randint

class Population:
	def __init__(self, solutionsList):
		self.solutionsList = []
		for sol in solutionsList:
			self.solutionsList.append(sol)
		self.averageDistance = self.setAverageDistance()

	def setAverageDistance(self):
		if(len(self.solutionsList) > 0):
			sum = 0
			for sol in self.solutionsList:
				sum += sol.getDistancesSum()
			return float(sum / len(self.solutionsList))
		else:
			return 0
	
	def getAverageDistance(self):
		return self.averageDistance
	
	def getSolutions(self):
		return self.solutionsList
	
	def addSolution(self, sol):
		self.solutionsList.append(sol)
		self.averageDistance = self.setAverageDistance()
	
	def addSolutionsList(self, list):
		for solution in list:
			self.solutionsList.append(solution)
		self.averageDistance = self.setAverageDistance()
	
	def sortSolutions(self):
		self.solutionsList = sorted(self.solutionsList, key = lambda Solution : Solution.distancesSum)
	
	def elitismSelection(self, percentage):
		listOfSolutions = []
		for i in range(int(len(self.solutionsList)*percentage)):
			listOfSolutions.append(self.solutionsList[i])
		return listOfSolutions
	
	def roulletteSelection(self, percentage):
		listOfSolutions = []
		s1 = 0
		for solution in self.solutionsList:
			s1 += solution.getDistancesSum()

		for i in range(int(len(self.solutionsList)*percentage)):
			r = randint(0, int(s1))
			s2 = 0
			j = 0
			while s2 <= r:
				s2 += self.solutionsList[j].getDistancesSum()
				j += 1
			j -= 1
			listOfSolutions.append(self.solutionsList[j])
		return listOfSolutions
	
	def putFirstTownOfEachSolutionOnList(self):
		for solution in self.solutionsList:
			solution.addFirstTown()
	
	def removeLastTownOfEachSolution(self):
		for solution in self.solutionsList:
			solution.removeLastTown()
	
	def reduce(self, n):
		while(len(self.solutionsList) > n):
			del self.solutionsList[-1]