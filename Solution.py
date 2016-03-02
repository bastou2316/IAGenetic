from Town import Town
from math import pow, sqrt
from random import randint

def prepareListToCross(list, listOfTownsToPutOnCrossZone, start, stop):
			
	listLength = len(list)		
	nbOfTownsOnCrossZone = len(listOfTownsToPutOnCrossZone)
	nbOfTownsInGoodPostion = 0

	while nbOfTownsInGoodPostion < nbOfTownsOnCrossZone:

		nbOfTownsInGoodPostion = 0
		#check how much towns are on cross sone and have to be there
		for i in range(start, stop):
			if(list[i].name in listOfTownsToPutOnCrossZone):
				nbOfTownsInGoodPostion += 1

		if(nbOfTownsInGoodPostion == nbOfTownsOnCrossZone):
			break		
		
		#if no one in cross zone, complete shift row
		if(nbOfTownsInGoodPostion == 0):
			list = shiftLeft(list, 1)
		###
		elif((stop - start) > 1):
			listOfTownsBeforeCrossZone = []
			listOfTownsInGoodPosition = []
			listOfTownsInCrossZoneToShift = []
			listOfTownAfterCrossZoneToShift = []
			listOfTownAfterCrossZoneToNotShift = []
			i = 0
			indexAfterTownsInGoodPosition = 0
			while i < start:
				listOfTownsBeforeCrossZone.append(list[i])
				i += 1
			while i < stop:
				if (list[i].name in listOfTownsToPutOnCrossZone):
					listOfTownsInGoodPosition.append(list[i])
				else:
					#listOfTownsBeforeCrossZone.append(list[i])
					listOfTownsInCrossZoneToShift.append(list[i])
				i += 1
			indexAfterTownsInGoodPosition = i
			while i < listLength:
				if(list[i].name in listOfTownsToPutOnCrossZone):
					listOfTownAfterCrossZoneToShift.append(list[i])
				else:
					listOfTownAfterCrossZoneToNotShift.append(list[i])
				i += 1
			
			if(start != 0):
				list = 	(
						listOfTownsBeforeCrossZone[1:] +
						listOfTownsInCrossZoneToShift +
						listOfTownsInGoodPosition +
						listOfTownAfterCrossZoneToShift +
						listOfTownAfterCrossZoneToNotShift +
						listOfTownsBeforeCrossZone[:1]
						)
			else:
				list = 	(
						listOfTownsInCrossZoneToShift[1:] +
						listOfTownsInGoodPosition +
						listOfTownAfterCrossZoneToShift +
						listOfTownAfterCrossZoneToNotShift +
						listOfTownsInCrossZoneToShift[:1]
						)
	return list

def shiftLeft(l, n):
		n = n % len(l)
		return l[n:] + l[:n]

class Solution:
	def __init__(self, townsList):
		self.townsList = []
		for t in townsList:
			self.townsList.append(t)
		self.distancesSum = self.checkPathDistance()
	
	def addTown(self, t):
		self.townsList.append(t)
		self.distancesSum = self.checkPathDistance()
	
	def addFirstTown(self):
		t = self.townsList[0]
		self.townsList.append(t)
		self.distancesSum = self.checkPathDistance()
	
	def removeLastTown(self):
		if(len(self.townsList) > 0):
			del self.townsList[-1]
			self.distancesSum = self.checkPathDistance()
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

	def crossover(self, solution2):

		sizeList1 = len(self.townsList)
		sizeList2 = len(solution2.townsList)
		if(sizeList1 == sizeList2):
			startPos = randint(0, (sizeList1 - 2))
			endPos = randint((startPos + 1), (sizeList1))

			listA = []
			listB = []
			for i in range(0, sizeList1):
				t1 = self.townsList[i]
				t2 = solution2.townsList[i]
				listA.append(Town(t1.name, t1.x, t1.y))
				listB.append(Town(t2.name, t2.x, t2.y))
			
			listOfTownsToPutFromListAOnListB = []
			listOfTownsToPutFromListBOnListA = []
			for i in range(startPos, endPos):
				listOfTownsToPutFromListAOnListB.append(listA[i].name)
				listOfTownsToPutFromListBOnListA.append(listB[i].name)

			listA = prepareListToCross(listA, listOfTownsToPutFromListBOnListA, startPos, endPos)

			listB = prepareListToCross(listB, listOfTownsToPutFromListAOnListB, startPos, endPos)

			childListA = []
			childListB = []
			
			childListA = (listA[:startPos] + solution2.townsList[startPos:endPos] + listA[endPos:])
			childListB = (listB[:startPos] + self.townsList[startPos:endPos] + listB[endPos:])

			return Solution(childListA), Solution(childListB)
		
	#swap two towns
	def mutate(self):
		a = randint(0, (len(self.townsList)-1))
		b = a
		
		while b == a:
			b = randint(0, (len(self.townsList)-1))

		listOfTowns = []
		for town in self.townsList:
			listOfTowns.append(town)
		
		temp = listOfTowns[a]
		listOfTowns[a] = listOfTowns[b]
		listOfTowns[b] = temp
		return Solution(listOfTowns)