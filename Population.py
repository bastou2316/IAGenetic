from random import randint

class Population:
	def __init__(self, solutionsList):
		self.solutionsList = []
		for sol in solutionsList:
			self.solutionsList.append(sol)
		self.averageDistance = self.setAverageDistance()

	def setAverageDistance(self):
		sum = 0
		for sol in self.solutionsList:
			sum += sol.getDistancesSum()
		return float(sum / len(self.solutionsList))
	
	def getAverageDistance(self):
		return self.averageDistance
	
	def getSolutions(self):
		return self.solutionsList
	
	def addSoluttion(self, sol):
		self.solutionsList.append(sol)
	
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
		