import numpy as np

from PIL import Image

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

import random

import math

import numpy as np

import sys


def showMap(terrainMap,go=None):
        
    if terrainMap.dtype == np.float64:
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

    else: 

        imagearray = np.zeros([terrainMap.shape[0], terrainMap.shape[1], 3])

        currentx = 0
    
        currenty = 0

        while currenty < (terrainMap).shape[0]:

            if terrainMap[currenty, currentx] == False:

                imagearray[currenty, currentx, :] = np.array([0,0,0])

            else: 

                imagearray[currenty, currentx, :] = np.array([255,255,255])

            currentx+=1

            if currentx == (terrainMap).shape[1]:

                currentx = 0

                currenty += 1

        plt.imshow(imagearray.astype('uint8'))

        plt.show()

def coordinatesRange(range):
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T

class Game():

    def __init__(self):
        
        self.terrainMap = np.load("algoarenamap1.npy")
        self.mapsizex = (self.terrainMap).shape[1]
        self.mapsizey = (self.terrainMap).shape[0]
        self.unitmap = np.zeros([self.mapsizey, self.mapsizex])
        self.team1startcoordsx = 15
        self.team1startcoordsy = 47
        self.team2startcoordsx = 160-15
        self.team2startcoordsy = 47
        self.team1 = Team(self.team1startcoordsx,self.team1startcoordsy,self.terrainMap)
        self.team2 = Team(self.team2startcoordsx,self.team2startcoordsy,self.terrainMap)
        self.trees = []
        self.goList = []

        self.walkableMapCreation()
        self.waterMapCreation()
        self.mineableMapCreation()
        self.goList = self.team1.buildings+self.team1.units+self.team2.buildings+self.team2.units+self.trees
        self.treeGeneration()
        self.goList = self.team1.buildings+self.team1.units+self.team2.buildings+self.team2.units+self.trees

        self.accesibleMapCreation()
        self.unitDisplay()
        showMap(self.unitMap)


    def gametick(self):

        self.goList = self.team1.buildings+self.team1.units+self.team2.buildings+self.team2.units+self.trees


    def showMap(self,mapIn):
        showMap(mapIn)
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
                coordinates = coordinatesRange(go.rad) + np.array([go.x,go.y])
                for coordinate in coordinates:
                    if 0 <= coordinate[1] and coordinate[1] < self.mapsizey and 0 <= coordinate[0] and coordinate[0] < self.mapsizex:
                        self.unitTruth[int(coordinate[1]),int(coordinate[0])] = False
            else: 
                self.unitTruth[go.y,go.x] = False

        self.accesibleTiles = np.logical_and(self.unitTruth,self.walkableTerrain)


    def treeGeneration(self):

        grassArea = (self.terrainMap == 3) | (self.terrainMap == 4)

        unitTruth = np.zeros([self.mapsizey, self.mapsizex]) == 0


        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.sumrad) + np.array([go.x,go.y])

                for coordinate in coordinates:
                    if 0 <= coordinate[1] and coordinate[1] < self.mapsizey and 0 <= coordinate[0] and coordinate[0] < self.mapsizex:
                        unitTruth[int(coordinate[1]),int(coordinate[0])] = False
            else: 
                unitTruth[go.y,go.x] = False


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
                self.trees.append(Tree(randx,randy))
                coordinates = coordinatesRange(treerad) + np.array([randx,randy])
                for coordinate in coordinates:
                    if 0 <= coordinate[1] and coordinate[1] < self.mapsizey and 0 <= coordinate[0] and coordinate[0] < self.mapsizex:
                        plantableArea[int(coordinate[1]),int(coordinate[0])] = False
                treecount+=1
            i+=1                



    def unitDisplay(self):
        self.unitMap = np.ones([self.mapsizey, self.mapsizex]) 
        print(self.unitMap)
        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array([go.x,go.y])
                for coordinate in coordinates:

                    if 0 <= coordinate[1] and coordinate[1] < self.mapsizey and 0 <= coordinate[0] and coordinate[0] < self.mapsizex:
                        self.unitMap[int(coordinate[1]),int(coordinate[0])] = 0
                pass
            else: 
                self.unitMap[go.y,go.x] = 0

        self.unitMap = self.unitMap *  self.terrainMap

        


                


class Team():

    def __init__(self,x,y,mapIn):

        self.visiblecoordinateslist = []

        self.units = []

        self.buildings = []

        self.visibleUnits = []   

        self.visibleBuildings = []  
        
        self.visibleTrees = []

        self.buildings.append(Castle(x,y))

        self.vistiles = np.zeros([mapIn.shape[0], mapIn.shape[1]])


    def visibility(self,mapIn,units,buildings):
        coordlist = []
        for building in self.buildings:
            coordinates = coordinatesRange(building.vision_range) + np.array([building.x,building.y])
            coordlist = coordlist + ((coordinates.tolist()))
        for unit in self.units:

            coordinates = coordinatesRange(unit.vision_range) + np.array([unit.x,unit.y])
            coordlist = coordlist + ((coordinates.tolist()))


        for pairs in coordlist:
            if 0 <= pairs[1] and pairs[1] < mapIn.shape[0] and 0 <= pairs[0] and pairs[0] < mapIn.shape[1]:
                self.vistiles[int(pairs[1]),int(pairs[0])] = 1

        self.visibleUnits = []+ self.units
        for unit in units:

            if self.vistiles[unit.y,unit.x] == 1: 
                self.visibleUnits.append(unit)

        self.visibleBuildings = [] + self.buildings
        for building in buildings:
            
            coordinates = coordinatesRange(building.rad) + np.array([building.x,building.y])
            for coordinates in coordinates:
                if self.vistiles[coordinates[1],coordinates[0]]  == 1:
                    self.visibleBuildings.append(building)
                    break

class GameObject():

    

    defaultHealth = 10
    
    possible_actions = set()

    def __init__(self, x, y):

        self.color = np.array([0,0,0])
        
        self.health = self.defaultHealth

        self.x = x

        self.y = y

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


    def __init__(self, x, y):
        self.color = np.array([0, 200, 0])

        super().__init__(x,y)


class Units(GameObject):

    def __init__(self, x, y, team):

        super().__init__(x,y)

        possible_actions = {"move_up","move_down","move_left","move_right"}

        self.team = team

        self.canAttack = True

        self.damage = 1

        self.speed = 1

        self.cooldown = 1

        self.range = 2

        self.vision_range = 4


    def move_up(self,mapIn):

        # if(mapIn[self.y-1,self.x]==1):

            self.y-=1



    def move_down(self,mapIn):

        # if(mapIn[self.y+1,self.x]==1):

            self.y+=1



    def move_right(self,mapIn):

        # if(mapIn[self.y,self.x+1]==1):

            self.x+=1

    def move_left(self,mapIn):

        # if(mapIn[self.y,self.x-1]==1):

            self.x-=1



    def move_to(self):

        pass

    def _attack(self, ennemy):

        # jsp quoi faire

        if (ennemy.pos < self.range):

            pass





class UtilityUnits(Units):

    def __init__(self, x, y):

        super().__init__(x,y)





class Worker(UtilityUnits):

    def __init__(self, x, y):

        super().__init__(x,y)

        self.x = x

        self.y = y

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

    def __init__(self, x, y, team):

        super().__init__(team)

        self.x = x

        self.y = y

        self.canAttack = False

        self.health = 10

        self.damage = 0

        self.speed = 10





class CombatUnits(GameObject):

    pass





class Melee(CombatUnits):

    def __init__(self, x, y, team):

        super().__init__(team)

        self.x = x

        self.y = y

        self.health = 20

        self.damage = 5

        self.speed = 5

        self.cooldown = 2





class Tank(CombatUnits):

    def __init__(self, x, y, team):

        super().__init__(team)

        self.x = x

        self.y = y

        self.health = 40

        self.damage = 5

        self.speed = 3

        self.cooldown = 3





class Archer(CombatUnits):

    def __init__(self, x, y, team):

        super().__init__(team)

        self.x = x

        self.y = y

        self.health = 15

        self.damage = 5

        self.speed = 5

        self.cooldown = 2

        self.bulletSpeed = 6





class GlassCannon(CombatUnits):

    def __init__(self, x, y, team):

        super().__init__(team)

        self.x = x

        self.y = y

        self.health = 5

        self.damage = 15

        self.speed = 10

        self.cooldown = 1

        self.bulletSpeed = 10





class Building(GameObject):

    def __init__(self,x,y):

        super().__init__(x,y)

        self.rad = 3

        self.sumrad = 5

        self.x = x

        self.y = y





class Castle(Building):

    def __init__(self,x,y):
        self.possibleactions = {"create_worker","create_scout"}

        super().__init__(x,y)

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


