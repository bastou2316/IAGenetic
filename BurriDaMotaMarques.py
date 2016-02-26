from Town import Town
from Problem import Problem
from Solution import Solution
from Population import Population

from random import randint, shuffle


def parsePositions(fname):
	arr = []
	with open(fname) as f:
		for line in f.readlines():
			posTab = line.split()
			t = Town(posTab[0], posTab[1], posTab[2])
			arr.append(t)
	return arr
	
def problemsGeneration(listOfTowns):
	probList = []
	tempList = []
	maxNbOfProblems = fact(len(listOfTowns))
	i = 0
		
	while (i < NB_OF_PROBLEMS and i < maxNbOfProblems):
		tempList = shuffleList(listOfTowns)
		if tempList not in probList:
			tempList.append(tempList[0])
			"""
			for t in tempList:
				print("%s   "%t.name, end="")
			print("\n")
			"""
			probList.append(Problem(tempList))
			i += 1
	return probList

def fact(n):
    if n < 2:
        return 1
    else:
        return n*fact(n-1)

def shuffleList(alist):
	a = alist[:]
	shuffle(a)
	return a

def generateNextGeneration(pop):
	elitismList = pop.elitismSelection(ELITISM_SELECTION_PERCENTAGE)
	
	print("\n\nelitism selection\n")
	for sol in elitismList:
		for town in sol.townsList:
			print("%s   "%town.name, end="")
		print("\ntotal distance = %d" % sol.getDistancesSum())
	
	roulletteList = pop.roulletteSelection(ROULLETTE_SELECTION_PERCENTAGE)
	
	print("\n\nroullette selection\n")
	for sol in roulletteList:
		for town in sol.townsList:
			print("%s   "%town.name, end="")
		print("\ntotal distance = %d" % sol.getDistancesSum())
	
	#newPopulation = Population(elitismList)

if __name__ == "__main__" :
	
	NB_OF_PROBLEMS = 10
	ELITISM_SELECTION_PERCENTAGE = 40 / 100
	ROULLETTE_SELECTION_PERCENTAGE = 1 - ELITISM_SELECTION_PERCENTAGE
	problemsList = []
	solutionsList = []
	
	file = "./Ressources12/data/pb005.txt"
	townsList = parsePositions(file)
	
	for town in townsList:
		print("Town %s: x = %s, y = %s" % (town.name, town.x, town.y))
	
	problemsList = problemsGeneration(townsList)
	
	for problem in problemsList:
		solutionsList.append(Solution(problem.townsList))

	population = Population(solutionsList)
	
	"""
	for sol in population.getSolutions():
		for town in sol.townsList:
			print("%s   "%town.name, end="")
		print("\ntotal distance = %d" % sol.distancesSum)
	"""

	population.sortSolutions()
	
	"""
	print("\n\nAfter Sort:\n")
	
	for sol in population.getSolutions():
		for town in sol.townsList:
			print("%s   "%town.name, end="")
		print("\ntotal distance = %d" % sol.getDistancesSum())
	print("\npopulation average distance = %d" % population.getAverageDistance())
	"""
	generateNextGeneration(population)
	