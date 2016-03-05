#########################################################
#	authors: Bastien Burri, Fabio Manuel da Mota Marques
#########################################################

from math import pow, sqrt
import ast
from random import randint, shuffle
from time import time
from os import system
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import argparse


#########################################################
#						classes
#########################################################

class Population:
    def __init__(self, solutionsList):
        self.solutionsList = []
        for sol in solutionsList:
            self.solutionsList.append(sol)
        self.averageDistance = self.setAverageDistance()

    def setAverageDistance(self):
        if (len(self.solutionsList) > 0):
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
        self.solutionsList = sorted(self.solutionsList, key=lambda Solution: Solution.distancesSum)

    def elitismSelection(self, percentage):
        listOfSolutions = []
        for i in range(int(len(self.solutionsList) * percentage)):
            listOfSolutions.append(self.solutionsList[i])
        return listOfSolutions

    def roulletteSelection(self, percentage):
        listOfSolutions = []
        s1 = 0
        for solution in self.solutionsList:
            s1 += solution.getDistancesSum()

        for i in range(int(len(self.solutionsList) * percentage)):
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
        while (len(self.solutionsList) > n):
            del self.solutionsList[-1]


class Solution:
    def __init__(self, townsList):
        self.townsList = []
        for t in townsList:
            self.townsList.append(t)
        self.distancesSum = self.checkPathDistance()

    def __str__(self):
        chaine = ",".join(str(x) for x in self.townsList)
        return "[" + chaine + "]"

    def addFirstTown(self):
        t = self.townsList[0]
        self.townsList.append(t)
        self.distancesSum = self.checkPathDistance()

    def checkPathDistance(self):
        sum = 0
        for x in range(len(self.townsList) - 1):
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
        if (sizeList1 == sizeList2):
            startPos = randint(0, (sizeList1 - 2))
            endPos = randint((startPos + 1), (sizeList1))

            # deepCopy loop
            listA = []
            listB = []
            for i in range(0, sizeList1):
                t1 = self.townsList[i]
                t2 = solution2.townsList[i]
                listA.append(Town(t1.name, t1.x, t1.y))
                listB.append(Town(t2.name, t2.x, t2.y))

                # check of what towns have to be putted on cross zone
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

            # swap two towns

    def mutate(self):
        townsListLength = len(self.townsList)

        listOfTowns = []
        for town in self.townsList:
            listOfTowns.append(town)

        a = randint(0, (townsListLength - 1))
        b = a
        while b == a:
            b = randint(0, (townsListLength - 1))

        temp = listOfTowns[a]
        listOfTowns[a] = listOfTowns[b]
        listOfTowns[b] = temp
        return Solution(listOfTowns)


class Problem:
    def __init__(self, townsList):
        self.townsList = townsList


class Town:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


#########################################################
#			methods for pygame use
#########################################################

screen_y = 500
screen_x = 500
cities = []

city_color = [10, 10, 200]  # blue
city_radius = 3
font_color = [255, 255, 255]  # white
window = pygame.display.set_mode((screen_x, screen_y))
screen = pygame.display.get_surface()


def freeze():
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break

		
def windows_init():
    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)


def draw(positions, screen, font, city_color, city_radius, font_color):
    screen.fill(0)
    for pos in positions:
        pygame.draw.circle(screen, city_color, pos, city_radius)
    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def create_problem(cities, screen, font, city_color, city_radius, font_color):
    draw(cities, screen, font, city_color, city_radius, font_color)

    collecting = True

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(pygame.mouse.get_pos())
                draw(cities, screen, font, city_color, city_radius, font_color)


def update_windows(screen, city_color, cities, font_color, font):
    screen.fill(0)
    pygame.draw.lines(screen, city_color, True, cities)
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()
		

#########################################################
#			methods for genetic algorithm
#########################################################

# function that prepare a list of towns for crossover
def prepareListToCross(list, listOfTownsToPutOnCrossZone, start, stop):
    listLength = len(list)
    nbOfTownsOnCrossZone = len(listOfTownsToPutOnCrossZone)
    nbOfTownsInGoodPostion = 0

    # loop for put all towns on cross zone
    while nbOfTownsInGoodPostion < nbOfTownsOnCrossZone:

        nbOfTownsInGoodPostion = 0
        # check how much towns are on cross sone and have to be there
        for i in range(start, stop):
            if (list[i].name in listOfTownsToPutOnCrossZone):
                nbOfTownsInGoodPostion += 1

        if (nbOfTownsInGoodPostion == nbOfTownsOnCrossZone):
            break

            # if no one in cross zone, complete shift row
        if (nbOfTownsInGoodPostion == 0):
            list = shiftLeft(list, 1)

            # if stop - start == 1, left shifts are enough
        elif ((stop - start) > 1):
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
                    # listOfTownsBeforeCrossZone.append(list[i])
                    listOfTownsInCrossZoneToShift.append(list[i])
                i += 1
            indexAfterTownsInGoodPosition = i
            while i < listLength:
                if (list[i].name in listOfTownsToPutOnCrossZone):
                    listOfTownAfterCrossZoneToShift.append(list[i])
                else:
                    listOfTownAfterCrossZoneToNotShift.append(list[i])
                i += 1

            if (start != 0):
                list = (
                    listOfTownsBeforeCrossZone[1:] +
                    listOfTownsInCrossZoneToShift +
                    listOfTownsInGoodPosition +
                    listOfTownAfterCrossZoneToShift +
                    listOfTownAfterCrossZoneToNotShift +
                    listOfTownsBeforeCrossZone[:1]
                )
            else:
                list = (
                    listOfTownsInCrossZoneToShift[1:] +
                    listOfTownsInGoodPosition +
                    listOfTownAfterCrossZoneToShift +
                    listOfTownAfterCrossZoneToNotShift +
                    listOfTownsInCrossZoneToShift[:1]
                )
    return list


# function that makes a left shift on a list
def shiftLeft(l, n):
    n = n % len(l)
    return l[n:] + l[:n]


# function that parse towns from a file
def parseTownsFromFile(fname):
    arr = []
    with open(fname) as f:
        for line in f.readlines():
            posTab = line.split()
            t = Town(posTab[0], posTab[1], posTab[2])
            arr.append(t)
    return arr


# function that parse towns from a file used in GUI interface
def parseTownsFromFile_GUI(fname):
    arr = []
    with open(fname) as f:
        for line in f.readlines():
            posTab = line.split()
            t = (posTab[1], posTab[2])
            arr.append(t)
    return arr


# function that generates diferent problems
def problemsGeneration(listOfTowns):
    probList = []
    tempList = []
    maxNbOfProblems = factorial(len(listOfTowns))
    i = 0

    while (i < NB_OF_PROBLEMS and i < maxNbOfProblems):
        tempList = shuffleList(listOfTowns)
        if tempList not in probList:
            # tempList.append(tempList[0])
            probList.append(Problem(tempList))
            i += 1
    return probList


# function that calculate the faxtorial of n (n!), useful for short lists of towns
def factorial(n):
    if n < 2:
        return 1
    else:
        return n * factorial(n - 1)


# function that shuffle a list
def shuffleList(alist):
    a = alist[:]
    shuffle(a)
    return a


# function that selects a part of a population with a percentage of elitism and roullette algorihma
def selection(pop):
    elitismList = pop.elitismSelection(ELITISM_SELECTION_PERCENTAGE)
    roulletteList = pop.roulletteSelection(ROULLETTE_SELECTION_PERCENTAGE)

    return Population(elitismList + roulletteList)


# function thah generates combinations of a selected population
def crossover(popu):
    newPopulation = Population([])
    solveList = popu.getSolutions()
    solutionsListLength = len(solveList)

    for i in range(0, (solutionsListLength - 1)):
        for j in range(i, solutionsListLength):
            childA, childB = solveList[i].crossover(solveList[j])
            newPopulation.addSolution(childA)
            newPopulation.addSolution(childB)

    return newPopulation


# function that genetrates a muttaion for each solution of a popuplation
def mutation(popul):
    mutatedList = []
    for solution in popul.getSolutions():
        mutatedList.append(solution.mutate())
    return Population(mutatedList)


# function with main loop of geenetic algorithm
def solve(file, gui, maxtime):
    startTime = time()
    problemsList = []
    solutionsList = []
    noBetterSolutionNumber = 0
    bestSolution = 0

    if (file is not None):
        townsList = parseTownsFromFile(file)
    else:
        arrT = []
        T = Town("", cities[0][0], cities[0][1])
        arrT.append(T)

        for i in range(0, len(cities)):
            T = Town("V" + str(i), cities[i][0], cities[i][1])
            arrT.append(T)
        townsList = arrT
    problemsList = problemsGeneration(townsList)

    for problem in problemsList:
        solutionsList.append(Solution(problem.townsList))

    population = Population(solutionsList)

    population.sortSolutions()
    bestSolution = population.getSolutions()[0].getDistancesSum()

    i = 1
    # main loop
    while (time() - startTime) < maxtime and noBetterSolutionNumber < CONVERGENCE_NUMBER:

        system('cls')
        print("Processing genetic algorithm...")
        print(time() - startTime)

        # selection
        selectedPopulation = selection(population)

        # cross selected solutions
        crossPopulation = crossover(selectedPopulation)

        population.addSolutionsList(crossPopulation.getSolutions())

        # sort solutions list
        population.sortSolutions()

        # reducing of population
        # better path rest in population
        population.reduce(NB_OF_PROBLEMS)

        mutatedPopuplation = mutation(population)
        population.addSolutionsList(mutatedPopuplation.getSolutions())

        population.sortSolutions()

        population.reduce(NB_OF_PROBLEMS)

        if (population.getSolutions()[0].getDistancesSum() < bestSolution):
            bestSolution = population.getSolutions()[0].getDistancesSum()
            noBetterSolutionNumber = 0
        else:
            noBetterSolutionNumber += 1
		
        if(gui==True):

            font = pygame.font.Font(None, 30)
            mystring = str(population.getSolutions()[0])
            list = ast.literal_eval(mystring)
            update_windows(screen, city_color, list, font_color, font)
        # print("BESTSOL")
        # print(population.getSolutions()[0])
        i += 1

    if (noBetterSolutionNumber == CONVERGENCE_NUMBER):
        print("\nConverging")

    bestSolution = population.getSolutions()[0]
    bestSolution.addFirstTown()

    if (gui == True):
        print("Press a key to continue...")
        freeze()

    return bestSolution.getDistancesSum(), bestSolution.townsList


# main function of genetic algorithm
def ga_solve(file=None, gui=True, maxtime=0):
    if (file is None and gui == False):
        print("No file and no gui passed as argument")
        exit()

    elif (file is None and gui == True):
        pygame.init()
        font = pygame.font.Font(None, 30)
        pygame.display.set_caption('Exemple')
        create_problem(cities, screen, font, city_color, city_radius, font_color)
    else:
        townsList = parseTownsFromFile(file)
        if (gui == True):
            windows_init()
    return solve(file, gui, maxtime)

	
# command line parameters management
def parseParams():
    gui = True
    maxtime = 0

    parser = argparse.ArgumentParser('Genetic algorithm for PVC')
    parser.add_argument("-n", "--nogui", help="disables gui", action="store_true")
    parser.add_argument("-m", "--maxtime", type=int, help="sets a maximum time")
    parser.add_argument("filename", type=str, help="the name of the file containing a list of towns", nargs="?")

    args = parser.parse_args()
    if args.nogui is not None:
        gui = not args.nogui
    if args.maxtime is not None:
        maxtime = args.maxtime

    return gui, maxtime, args.filename


if __name__ == "__main__":

    # sys.path.append(r"C:\Python351\Lib\site-packages\pygame")

    townsList = []
    NB_OF_PROBLEMS = 10
    CONVERGENCE_NUMBER = 300
    ELITISM_SELECTION_PERCENTAGE = 60 / 100
    ROULLETTE_SELECTION_PERCENTAGE = 1 - ELITISM_SELECTION_PERCENTAGE

    GUI, MAXTIME, FILENAME = parseParams()

    distance, listOfTowns = ga_solve(FILENAME, GUI, MAXTIME)
    print("\n\nBest result:\n")
    for town in listOfTowns:
        print("%s   " % town.name)
    print("\ntotal distance = %d" % distance)
