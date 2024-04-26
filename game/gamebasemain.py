import copy
import numpy as np

from PIL import Image
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import random
import math
import numpy as np
import sys
import player1
import showmaps

unitActionTypes = {0: "move_to", 1: "gather_resource", 2: "attack", 3: "build"}


def nextPosition(startPosition, endPosition, availablePositionMatrix):

    min_value = float('inf')
    next_pos = startPosition

    
    weightMatrix = djistras(startPosition, endPosition, availablePositionMatrix)

    if weightMatrix is not None:

        rows, cols = weightMatrix.shape
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = startPosition[0] + dx, startPosition[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if weightMatrix[nx, ny] < min_value:
                    min_value = weightMatrix[nx, ny]
                    next_pos = [nx, ny]
        return next_pos
    else: 
        return startPosition
  

def djistras(startPosition, endPosition, availablePositionMatrix):
    maxval = 10000
    availablePositionMatrix[startPosition[0],startPosition[1]] = True
    weightMatrix = np.zeros(availablePositionMatrix.shape) + maxval
    surroundset = set()

    weightMatrix[endPosition[0], endPosition[1]] = 0
    if availablePositionMatrix[endPosition[0]+1,endPosition[1]] == True:
        weightMatrix[endPosition[0]+1,endPosition[1]] = 1
        surroundset.add((endPosition[0]+1,endPosition[1]))
    if availablePositionMatrix[endPosition[0]-1,endPosition[1]] == True:
        weightMatrix[endPosition[0]-1,endPosition[1]] = 1
        surroundset.add((endPosition[0]-1,endPosition[1]))
    if availablePositionMatrix[endPosition[0],endPosition[1]+1] == True:
        weightMatrix[endPosition[0],endPosition[1]+1] = 1
        surroundset.add((endPosition[0],endPosition[1]+1))
    if availablePositionMatrix[endPosition[0],endPosition[1]-1] == True:
        weightMatrix[endPosition[0],endPosition[1]-1] = 1
        surroundset.add((endPosition[0],endPosition[1]-1))
    if availablePositionMatrix[endPosition[0]-1,endPosition[1]-1] == True:
        weightMatrix[endPosition[0]-1,endPosition[1]-1] = 1.414
        surroundset.add((endPosition[0]-1,endPosition[1]-1))
    if availablePositionMatrix[endPosition[0]+1,endPosition[1]-1] == True:
        weightMatrix[endPosition[0]+1,endPosition[1]-1] = 1.414
        surroundset.add((endPosition[0]+1,endPosition[1]-1))
    if availablePositionMatrix[endPosition[0]-1,endPosition[1]+1] == True:
        weightMatrix[endPosition[0]-1,endPosition[1]+1] = 1.414
        surroundset.add((endPosition[0]-1,endPosition[1]+1))
    if availablePositionMatrix[endPosition[0]+1,endPosition[1]+1] == True:
        weightMatrix[endPosition[0]+1,endPosition[1]+1] = 1.414
        surroundset.add((endPosition[0]+1,endPosition[1]+1))
    counter = 1 
    while weightMatrix[startPosition[0],startPosition[1]] == maxval and counter < 10000:
        tempnextset = set()
        counter+=1        
        for coords in surroundset:
            x, y = coords[0], coords[1]
            if availablePositionMatrix[x+1,y] == True:
                if weightMatrix[x+1,y] > weightMatrix[x,y] + 1:
                    weightMatrix[x+1,y] = weightMatrix[x,y] + 1
                    tempnextset.add((x+1,y))
            if availablePositionMatrix[x-1,y] == True:
                if weightMatrix[x-1,y] > weightMatrix[x,y] + 1:
                    weightMatrix[x-1,y] = weightMatrix[x,y] + 1
                    tempnextset.add((x-1,y))
            if availablePositionMatrix[x,y+1] == True:
                if weightMatrix[x,y+1] > weightMatrix[x,y] + 1:
                    weightMatrix[x,y+1] = weightMatrix[x,y] + 1
                    tempnextset.add((x,y+1))
            if availablePositionMatrix[x,y-1] == True:
                if weightMatrix[x,y-1] > weightMatrix[x,y] + 1:
                    weightMatrix[x,y-1] = weightMatrix[x,y] + 1
                    tempnextset.add((x,y-1))
            if availablePositionMatrix[x-1,y-1] == True:
                if weightMatrix[x-1,y-1] > weightMatrix[x,y] + 1.414:
                    weightMatrix[x-1,y-1] = weightMatrix[x,y] + 1.414
                    tempnextset.add((x-1,y-1))
            if availablePositionMatrix[x+1,y-1] == True:
                if weightMatrix[x+1,y-1] > weightMatrix[x,y] + 1.414:
                    weightMatrix[x+1,y-1] = weightMatrix[x,y] + 1.414
                    tempnextset.add((x+1,y-1))
            if availablePositionMatrix[x-1,y+1] == True:
                if weightMatrix[x-1,y+1] > weightMatrix[x,y] + 1.414:
                    weightMatrix[x-1,y+1] = weightMatrix[x,y] + 1.414
                    tempnextset.add((x-1,y+1))
            if availablePositionMatrix[x+1,y+1] == True:
                if weightMatrix[x+1,y+1] > weightMatrix[x,y] + 1.414:
                    weightMatrix[x+1,y+1] = weightMatrix[x,y] + 1.414
                    tempnextset.add((x+1,y+1))
                
        surroundset = tempnextset

    if counter == 10000:
        return None
    
    return weightMatrix


def coordinatesRange(range):
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T

class Player():

    def __init__(self):
        self.buildingActionTypes = {1: "summon"}

        self.myUnits = []
        self.myBuildings = []
        self.trees = []
        self.enemyUnits = []
        self.enemyBuildings = []

        self.summonRequests= []
        self.moveRequests = []
        self.attackUnitRequests = []
        self.attackBuildingRequests = []

        self.buildRequests = []
        self.gatherRequests = []

        self.wood = 0
        self.stone = 0

    def action(self):

        pass

    def reset(self):
        
        self.myUnits = []
        self.myBuildings = []
        self.trees = []
        self.enemyUnits = []
        self.enemyBuildings = []
        self.summonRequests= []
        self.moveRequests = []
        self.attackUnitRequests = []
        self.attackBuildingRequests = []

        self.buildRequests = []
        self.gatherRequests = []

        self.wood = 0
        self.stone = 0
    
class Game():

    def __init__(self):
        maxturns = 30
        turn = 0 
        self.frames = []
        self.player1 = Player()
        self.player2 = Player()
        self.terrainMap = np.load("algoarenamap1.npy")

        self.mapsizey = (self.terrainMap).shape[0]
        self.mapsizex = (self.terrainMap).shape[1]

        self.walkableMapCreation()
        self.waterMapCreation()
        self.mineableMapCreation()

        self.team1startcoords = [47,15]
        self.team2startcoords = [47,145]

        self.team1 = Team(self.team1startcoords)
        self.team2 = Team(self.team2startcoords)

        self.treeGeneration()

        # Game start !

        self.goListCreation()
        self.accesibleMapCreation()
        self.unitDisplay()
        self.updatePlayerInfo()

        self.player1.summonRequests.append([1,[30,30]])

        self.playerActions()
        self.runActions()

        self.goListCreation()
        self.accesibleMapCreation()
        self.unitDisplay()
        self.updatePlayerInfo()


        self.player1.moveRequests.append([0,[62,135]])

        self.playerActions()
        self.runActions()


        while turn < maxturns: 
            self.goListCreation()
            self.accesibleMapCreation()
            self.unitDisplay()
            self.playerActions()
            self.runActions()

            self.frames.append(self.unitMap)
            self.updatePlayerInfo()
            turn +=1
            
        print("Finished Simulation")
        showmaps.showImageList(self.frames)
        
    def updatePlayerInfo(self):
        self.player1.reset()
        for units in self.team1.units:
            self.player1.myUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates,
                    "goal": units.goal,
                    "currentaction": units.currentaction

                }
            )
        for buildings in self.team1.buildings:
            self.player1.myBuildings.append(
                {
                    "type": buildings.__class__.__name__,
                    "health": buildings.health,
                    "coordinates": buildings.coordinates
                }
            )
        self.player1.wood = self.team1.wood
        self.player1.stone = self.team1.stone
        for units in self.team2.units:
            self.player1.enemyUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates
                }
            )
        for buildings in self.team2.buildings:
            self.player1.enemyBuildings.append(
                {
                    "type": buildings.__class__.__name__,
                    "health": buildings.health,
                    "coordinates": buildings.coordinates
                }
            )

        self.player2.reset()
        for units in self.team2.units:
            self.player2.myUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates
                }
            )
        for buildings in self.team2.buildings:
            self.player2.myBuildings.append(
                {
                    "type": buildings.__class__.__name__,
                    "health": buildings.health,
                    "coordinates": buildings.coordinates
                }
            )
        self.player2.wood = self.team2.wood
        self.player2.stone = self.team2.stone
        for units in self.team1.units:
            self.player2.enemyUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates
                }
            )
        for buildings in self.team1.buildings:
            self.player2.enemyBuildings.append(
                {
                    "type": buildings.__class__.__name__,
                    "health": buildings.health,
                    "coordinates": buildings.coordinates
                }
            )

    def walkableMapCreation(self):
        self.walkableTerrain = (self.terrainMap == 2) | (self.terrainMap == 3) | (self.terrainMap == 4) | (self.terrainMap == 9)
    def waterMapCreation(self):
        self.waterTerrain = (self.terrainMap == 1)
    def mineableMapCreation(self):
        self.rockTerrain = (self.terrainMap == 5) | (self.terrainMap == 6) | (self.terrainMap == 7) | (self.terrainMap == 8)

    def goListCreation(self):
        self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units

    def accesibleMapCreation(self):
        self.unitTruth = np.zeros([self.mapsizey, self.mapsizex]) == 0
        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array(go.coordinates)
                for coordinate in coordinates:
                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        self.unitTruth[int(coordinate[0]),int(coordinate[1])] = False
            else: 
                self.unitTruth[go.coordinates[0] , go.coordinates[1]] = False

        self.accesibleTiles = np.logical_and(self.unitTruth,self.walkableTerrain)

    def treeGeneration(self):

        self.trees = []

        grassArea = (self.terrainMap == 3) | (self.terrainMap == 4)

        unitTruth = np.zeros([self.mapsizey, self.mapsizex]) == 0

        for go in (self.team1.buildings + self.team2.buildings):
            
            coordinates = coordinatesRange(go.sumrad) + np.array(go.coordinates)

            for coordinate in coordinates:
                if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                    unitTruth[int(coordinate[0]),int(coordinate[1])] = False

        accesibleTiles = np.logical_and(unitTruth,self.walkableTerrain)

        plantableArea = np.logical_and(grassArea,accesibleTiles)

        maxtree = 1000
        treecount = 0
        maxiterations = 100000
        treerad = 3
        i=0
        
        while treecount < maxtree and i < maxiterations:

            randx = random.randint(0,self.mapsizex-1)
            randy = random.randint(0,self.mapsizey-1)
            

            if plantableArea[randy,randx]:
                self.trees.append(Tree([randy,randx]))
                coordinates = coordinatesRange(treerad) + np.array([randy,randx])
                for coordinate in coordinates:
                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        plantableArea[int(coordinate[0]),int(coordinate[1])] = False
                treecount+=1
            i+=1                

    def unitDisplay(self):
        self.unitMap = copy.deepcopy(self.terrainMap)
        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array(go.coordinates)
                for coordinate in coordinates:

                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        if go in self.team1.buildings:
                            self.unitMap[int(coordinate[0]),int(coordinate[1])] = 10
                        if go in self.team2.buildings:
                            self.unitMap[int(coordinate[0]),int(coordinate[1])] = 11
            elif issubclass(go.__class__,Tree):
                self.unitMap[go.coordinates[0],go.coordinates[1]] = 12
            else: 
                if go in self.team1.units:
                    self.unitMap[go.coordinates[0],go.coordinates[1]] = 10
                if go in self.team2.units:
                    self.unitMap[go.coordinates[0],go.coordinates[1]] = 11

    def playerActions(self):
        for requests in self.player1.moveRequests:
            self.team1.units[requests[0]].goal = "move_to"
            self.team1.units[requests[0]].currentaction = "move_to"
            self.team1.units[requests[0]].argument = requests[1]
            
        for requests in self.player1.summonRequests:
            self.team1.summonType = requests[0]
            self.team1.summonLocation = requests[1]
    
    def runActions(self):

        for units in self.team1.units:
            units.action(self.accesibleTiles)
        
        self.team1.action()
                    
class Team():

    def __init__(self,coordinates):

        self.units = []

        self.buildings = []

        self.wood = 100

        self.stone = 100

        self.buildings.append(Castle(coordinates))

        self.summonLocation = None

        self.summonType = None

    def action(self):

        if self.summonType == 1:
            self.units.append(Worker(self.summonLocation))

        self.summonLocation = None

        self.summonType = None
        




class GameObject():

    def __init__(self, coordinates):

        self.possible_actions = set()

        self.health = 10

        self.coordinates = coordinates



class Tree(GameObject):


    def __init__(self, coordinates):

        super().__init__(coordinates)

class Units(GameObject):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.canAttack = True

        self.damage = 1

        self.speed = 1

        self.cooldown = 1

        self.cooldowncounter = 0

        self.range = 2

        self.vision_range = 4
        
        self.goal = None

        self.currentaction = None

        self.argument = None
    

class UtilityUnits(Units):

    def __init__(self, coordinates):

        super().__init__(coordinates)

class Worker(UtilityUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.coordinates = coordinates

        self.health = 10

        self.damage = 1

        self.speed = 3

        self.cooldown = 2

    def action(self,availableposition):
        if self.goal == "move_to":
            if self.coordinates != self.argument:
                nextpos = nextPosition(self.coordinates,self.argument,availableposition)
                if nextpos == self.coordinates:
                    self.currentaction = None
                    self.argument = None
                    self.goal = None
                else: 
                    self.coordinates = nextpos


class CombatUnits(GameObject):

    pass

class Melee(CombatUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)
        self.coordinates = coordinates
        self.health = 20
        self.damage = 5
        self.speed = 5
        self.cooldown = 2

class Building(GameObject):

    def __init__(self,coordinates):

        super().__init__(coordinates)

        self.rad = 3
        self.sumrad = 5
        self.coordinates = coordinates

class Castle(Building):

    def __init__(self,coordinates):

        super().__init__(coordinates)

        self.rad = 3
        self.sumrad = 5
        self.health = 10



