import numpy as np

from PIL import Image

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

import random

import math

import numpy as np

import sys
import player1

def nextPosition(startPosition, endPosition, availablePositionMatrix):

    min_value = float('inf')
    next_pos = startPosition
    print("start position: ", startPosition)
    print("end position: ", endPosition)
    
    weightMatrix = heatMap(startPosition, endPosition, availablePositionMatrix)

    if type(weightMatrix) != bool:

        rows, cols = weightMatrix.shape
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = startPosition[0] + dx, startPosition[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if weightMatrix[nx, ny] < min_value:
                    min_value = weightMatrix[nx, ny]
                    next_pos = [nx, ny]
        print("next position: ", next_pos)
        return next_pos
    else: 
        print(weightMatrix)
        return startPosition
  

def heatMap(startPosition, endPosition, availablePositionMatrix):
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
        return False
    
    return weightMatrix



def showHeatMap(weight,accessible,startPosition,endPosition,maxval):

    imagearray = np.zeros([accessible.shape[0], accessible.shape[1], 3])

    currentx = 0

    currenty = 0

    while currenty < (accessible).shape[0]:

        if accessible[currenty, currentx] == False:

            imagearray[currenty, currentx, :] = np.array([0,0,0])

        elif weight[currenty, currentx] == maxval:

            imagearray[currenty, currentx, :] = np.array([255,255,255])

        else: 

            imagearray[currenty, currentx, :] = np.array([0,0,255])

        currentx+=1

        if currentx == (accessible).shape[1]:

            currentx = 0

            currenty += 1

    imagearray[startPosition[0], startPosition[1], :] = np.array([0,255,0])
    imagearray[endPosition[0], endPosition[1], :] = np.array([255,0,0])


    plt.imshow(imagearray.astype('uint8'))

    plt.show()


def showBlackWhite(blackwhite):
    
    imagearray = np.zeros([blackwhite.shape[0], blackwhite.shape[1], 3])

    currentx = 0

    currenty = 0

    while currenty < (blackwhite).shape[0]:

        if blackwhite[currenty, currentx] == False:

            imagearray[currenty, currentx, :] = np.array([0,0,0])

        else: 

            imagearray[currenty, currentx, :] = np.array([255,255,255])

        currentx+=1

        if currentx == (blackwhite).shape[1]:

            currentx = 0

            currenty += 1

    plt.imshow(imagearray.astype('uint8'))

    plt.show()


def showMap(terrainMap):
        

    # Terrain types

    # 0 = fog

    # 1 = water

    # 2 = sand

    # 3 = grass1

    # 4 = grass2

    # 5 = stone1

    # 6 = stone2

    # 7 = stone3

    # 8 = stone4

    terrain_colors = {
        0: np.array([0, 0, 0]),          # fog
        1: np.array([0, 0, 255]),        # water
        2: np.array([255, 255, 0]),      # sand
        3: np.array([0, 255, 0]),        # grass1
        4: np.array([0, 255, 0]),        # grass2
        5: np.array([128, 128, 128]),    # stone1
        6: np.array([160, 160, 160]),    # stone2
        7: np.array([180, 180, 180]),    # stone3
        8: np.array([200, 200, 200]),    # stone4
        9: np.array([143, 101, 0])       # bridge
    }

    imagearray = np.zeros([terrainMap.shape[0], terrainMap.shape[1], 3])

    currentx = 0

    currenty = 0

    while currenty < (terrainMap).shape[0]:

        if terrainMap[currenty, currentx] in terrain_colors:

            imagearray[currenty, currentx, :] = terrain_colors[terrainMap[currenty, currentx]]

        currentx += 1

        if currentx == (terrainMap).shape[1]:

            currentx = 0

            currenty += 1

    plt.imshow(imagearray.astype('uint8'))

    plt.show()


def coordinatesRange(range):
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T

class Player():

    

class Game():

    def __init__(self):
        
        self.terrainMap = np.load("algoarenamap1.npy")
        self.mapsizex = (self.terrainMap).shape[1]
        self.mapsizey = (self.terrainMap).shape[0]
        self.unitmap = np.zeros([self.mapsizey, self.mapsizex])
        self.team1startcoords = [47,15]
        self.team2startcoords = [47,145]

        self.team1 = Team(self.team1startcoords,self.terrainMap)
        self.team2 = Team(self.team2startcoords,self.terrainMap)

        self.trees = []
        self.goList = []
        self.walkableMapCreation()
        self.waterMapCreation()
        self.mineableMapCreation()
        self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units
        self.treeGeneration()
        self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units
        self.accesibleMapCreation()
        self.unitDisplay()

        self.team1.newState(self.terrainMap,self.team2.units,self.team2.buildings)
        self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units
        self.team1.purchaseUnit([30,30])
        showMap(self.team1.vistiles*self.unitMap)
        self.team1.units[0].moveTo([62,135])

        while True: 
            self.accesibleMapCreation()
            self.unitDisplay()
            self.team1.newState(self.terrainMap,self.team2.units,self.team2.buildings)
            self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units
            self.team1.units[0].action(self.accesibleTiles)
            showMap(self.team1.vistiles*self.unitMap)







    def walkableMapCreation(self):
        self.walkableTerrain = (self.terrainMap == 2) | (self.terrainMap == 3) | (self.terrainMap == 4) | (self.terrainMap == 9)
    def waterMapCreation(self):
        self.waterTerrain = (self.terrainMap == 1)
    def mineableMapCreation(self):
        self.rockTerrain = (self.terrainMap == 5) | (self.terrainMap == 6) | (self.terrainMap == 7) | (self.terrainMap == 8)

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

        grassArea = (self.terrainMap == 3) | (self.terrainMap == 4)

        unitTruth = np.zeros([self.mapsizey, self.mapsizex]) == 0

        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.sumrad) + np.array(go.coordinates)

                for coordinate in coordinates:
                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        unitTruth[int(coordinate[0]),int(coordinate[1])] = False
            else: 
                unitTruth[go.coordinates] = False


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
        self.unitMap = np.ones([self.mapsizey, self.mapsizex]) 
        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array(go.coordinates)
                for coordinate in coordinates:

                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        self.unitMap[int(coordinate[0]),int(coordinate[1])] = 0
                pass
            else: 
                self.unitMap[go.coordinates[0],go.coordinates[1]] = 0

        self.unitMap = self.unitMap *  self.terrainMap

                    
class Team():

    def __init__(self,coordinates,mapIn):

        self.visiblecoordinateslist = []

        self.units = []

        self.buildings = []

        self.visibleUnits = []   

        self.visibleBuildings = []  
        
        self.visibleTrees = []

        self.wood = 100

        self.stone = 100

        self.buildings.append(Castle(coordinates))

        self.vistiles = np.zeros([mapIn.shape[0], mapIn.shape[1]])

    def newState(self,mapIn,units,buildings):

        coordlist = []
        for building in self.buildings:
            coordinates = coordinatesRange(building.vision_range) + np.array(building.coordinates)
            coordlist = coordlist + ((coordinates.tolist()))
        for unit in self.units:
            coordinates = coordinatesRange(unit.vision_range) + np.array(unit.coordinates)
            coordlist = coordlist + ((coordinates.tolist()))


        for pairs in coordlist:
            if 0 <= pairs[0] and pairs[0] < mapIn.shape[0] and 0 <= pairs[1] and pairs[1] < mapIn.shape[1]:
                self.vistiles[int(pairs[0]),int(pairs[1])] = 1

        self.visibleUnits = []+ self.units
        for unit in units:

            if self.vistiles[unit.coordinates[0],unit.coordinates[1]] == 1: 
                self.visibleUnits.append(unit)

        self.visibleBuildings = [] + self.buildings
        for building in buildings:
            
            coordinates = coordinatesRange(building.rad) + np.array(building.coordinates)
            for coordinates in coordinates:
                if self.vistiles[int(coordinates[0]),int(coordinates[1])]  == 1:
                    self.visibleBuildings.append(building)
                    break        


    def purchaseUnit(self,coordinates):
        self.units.append(Worker(coordinates))

class GameObject():

    defaultHealth = 10
    
    possible_actions = set()

    def __init__(self, coordinates):

        self.possible_actions = set()

        self.color = np.array([0,0,0])
        
        self.health = self.defaultHealth

 

        self.coordinates = coordinates

        self.action_queue = []

        self.vision_range = 4


    def _lose_health(self, damage):

        self.health -= damage

        if (self.health <= 0):

            dead = True

    def add_to_queue(self, action):
        
        if action not in self.possible_actions:
            print("Not in possible actions")
        else:
            self.action_queue.append(action)

    def _execute_next_action(self):

        """Execute the next action in the queue, if any."""

        if self.action_queue:
            
            action = self.action_queue.pop(0)

            # Here, add code to perform the action

        else:

            print("no actions to execute.")

class Tree(GameObject):


    def __init__(self, coordinates):
        self.color = np.array([0, 200, 0])

        super().__init__(coordinates)


class Units(GameObject):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        possible_actions = {"moving_to","attacking","gathering",}

        self.canAttack = True

        self.damage = 1

        self.speed = 1

        self.cooldown = 1

        self.range = 2

        self.vision_range = 4
        
        self.currentaction = None
        self.predicat = None

    def moveTo(self, coord):

        self.currentaction = "moving_to"
        self.predicat = coord
    
    def _action(self,availableposition):
        if self.currentaction == "moving_to":
            if self.coordinates != self.predicat:
                nextpos = nextPosition(self.coordinates,self.predicat,availableposition)
                print(nextpos)
                if nextpos == self.coordinates:
                    self.currentaction = None
                    self.predicat = None
                else: 
                    self.coordinates = nextpos
        
        

    def _attack(self, ennemy):

        # jsp quoi faire

        if (ennemy.pos < self.range):

            pass





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

    def _execute_next_action(self):

        """Execute the next action in the queue, if any."""

        if self.action_queue:
            
            action = self.action_queue.pop(0)

            if action == "move_up":
                self.move_up()
            elif action == "move_down":
                self.move_down()
            elif action == "move_left":
                self.move_left()
            elif action == "move_right":
                self.move_right
        else:

            print("no actions to execute.")





class Scout(UtilityUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.coordinates = coordinates

        self.canAttack = False

        self.health = 10

        self.damage = 0

        self.speed = 10





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





class Tank(CombatUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.coordinates = coordinates

        self.health = 40

        self.damage = 5

        self.speed = 3

        self.cooldown = 3





class Archer(CombatUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.coordinates = coordinates

        self.health = 15

        self.damage = 5

        self.speed = 5

        self.cooldown = 2

        self.bulletSpeed = 6





class GlassCannon(CombatUnits):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.coordinates = coordinates

        self.health = 5

        self.damage = 15

        self.speed = 10

        self.cooldown = 1

        self.bulletSpeed = 10





class Building(GameObject):

    def __init__(self,coordinates):

        super().__init__(coordinates)

        self.rad = 3

        self.sumrad = 5

        self.coordinates = coordinates





class Castle(Building):

    def __init__(self,coordinates):
        self.possibleactions = {"create_worker","create_scout"}

        super().__init__(coordinates)

        self.rad = 3
        self.sumrad = 5
        self.vision_range = 15
        self.color = np.array([160,160,160])
        self.health = 10


    def _CreateWorker(x, y, team):

        return Worker(x, y, team)

    def _CreateScout(x, y, team):

        return Scout(x, y, team)


def main():

    np.set_printoptions(threshold=sys.maxsize)


