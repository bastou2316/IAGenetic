from Town import Town
from math import pow, sqrt

def parsePositions(fname):
	arr = []
	with open(fname) as f:
		for line in f.readlines():
			posTab = line.split()
			t = Town(posTab[0], posTab[1], posTab[2])
			arr.append(t)
	return arr

def getSmallestDistanceBetweenTwoTowns(list):
	i = 0
	j = 1
	listLength = len(list)
	town1 = list[i]
	town2 = list[j]
	smallestDistance = euclidianDistanceBetweenTwoTowns(town1, town2)
	while(i < (listLength - 1)):
		j = i + 1
		while(j < listLength):
			x = euclidianDistanceBetweenTwoTowns(list[i], list[j])
			if(x < smallestDistance):
				smallestDistance = x
				town1 = list[i]
				town2 = list[j]
			j += 1
		i += 1
	return smallestDistance, town1, town2

def getSmallestDistanceBetweenTwoTownsFromATown(list, town):
	
	if(len(list) == 1):
		return 0, town, town
	else:
		i = 0
			
		while(list[i] == town):
			i += 1
			
		town2 = list[i]
		smallestDistance = euclidianDistanceBetweenTwoTowns(town, town2)	
		listLength = len(list)
		i += 1
		while(i < (listLength - 1)):
				if(town != list[i]):
					x = euclidianDistanceBetweenTwoTowns(town, list[i])
					if(x < smallestDistance):
						smallestDistance = x
						town2 = list[i]	
				i += 1
		return smallestDistance, town, town2
	
def euclidianDistanceBetweenTwoTowns(a, b):
	return float(sqrt(pow((int(a.x) - int(b.x)), 2) + pow((int(a.y) - int(b.y)), 2)))
	
if __name__ == "__main__" :
	
	file = "./Ressources12/data/pb010.txt"
	townsList = parsePositions(file)
	
	for town in townsList:
		print("Town %s: x = %s, y = %s" % (town.name, town.x, town.y))
	
	k = 0
	l = 1
	
	listLength = len(townsList)
	distance, townA, townB = getSmallestDistanceBetweenTwoTowns(townsList)
	print("the smallest distance is between %s and %s and equals %d" % (townA.name, townB.name, distance))
	townsList.remove(townA)
	

	while(len(townsList) > 1):
		distance, townA, townB = getSmallestDistanceBetweenTwoTownsFromATown(townsList, townB)
		print("the smallest distance is between %s and %s and equals %d" % (townA.name, townB.name, distance))
		townsList.remove(townA)	
	