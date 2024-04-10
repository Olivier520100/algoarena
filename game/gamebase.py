import numpy as np

from PIL import Image

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

import random

import math

import numpy as np

import sys

def showMap(displaymap,go=None):
        
    if displaymap.dtype == np.float64:
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
            4: np.array([0, 200, 0]),        # grass2
            5: np.array([128, 128, 128]),    # stone1
            6: np.array([160, 160, 160]),    # stone2
            7: np.array([180, 180, 180]),    # stone3
            8: np.array([200, 200, 200]),    # stone4
            9: np.array([143, 101, 0])       # bridge
        }

        imagearray = np.zeros([displaymap.shape[0], displaymap.shape[1], 3])

        currentx = 0

        currenty = 0

        while currenty < (displaymap).shape[0]:

            if displaymap[currenty, currentx] in terrain_colors:

                imagearray[currenty, currentx, :] = terrain_colors[displaymap[currenty, currentx]]

            currentx += 1

            if currentx == (displaymap).shape[1]:

                currentx = 0

                currenty += 1

        plt.imshow(imagearray.astype('uint8'))

        plt.show()

    else: 

        imagearray = np.zeros([displaymap.shape[0], displaymap.shape[1], 3])

        currentx = 0
    
        currenty = 0

        while currenty < (displaymap).shape[0]:

            if displaymap[currenty, currentx] == False:

                imagearray[currenty, currentx, :] = np.array([0,0,0])

            else: 

                imagearray[currenty, currentx, :] = np.array([255,255,255])

            currentx+=1

            if currentx == (displaymap).shape[1]:

                currentx = 0

                currenty += 1

        plt.imshow(imagearray.astype('uint8'))

        plt.show()

def coordinatesRange(range):
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T


class Map():

    def __init__(self):

        self.displaymap = np.load("algoarenamap1.npy")


        self.terrainmap = self.displaymap

        self.mapsizex = (self.displaymap).shape[1]

        self.mapsizey = (self.displaymap).shape[0]

        self.unitmap = np.zeros([self.mapsizey, self.mapsizex])


        self.usableMapCreation()

    def showMap(self):

        showMap(self.displaymap)
        showMap(self.accesibleMap)
        

    def usableMapCreation(self):
        self.usableterrain = (self.displaymap == 2) | (self.displaymap == 3) | (self.displaymap == 4) | (self.displaymap == 9)


    def accesibleTile(self,objlist):
        self.unitmap = np.zeros([self.mapsizey, self.mapsizex]) == 0
        for go in objlist:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array([go.x,go.y])
                for coordinate in coordinates:
                    
                    if 0 <= coordinate[1] and coordinate[1] < self.mapsizey and 0 <= coordinate[0] and coordinate[0] < self.mapsizex:
                        self.unitmap[int(coordinate[1]),int(coordinate[0])] = False
            else: 
                self.unitmap[go.y,go.x] = False



        self.accesibleMap = np.logical_and(self.unitmap,self.usableterrain )


    
        
    

class Game():

    def __init__(self):

        self.map = Map()
        self.team1startcoordsx = 15
        self.team1startcoordsy = 47
        self.team2startcoordsx = 160-15
        self.team2startcoordsy = 47
        self.team1 = Team(self.team1startcoordsx,self.team1startcoordsy,self.map.displaymap)
        self.team2 = Team(self.team2startcoordsx,self.team2startcoordsy,self.map.displaymap)
        self.trees = []
        self.goList = []

        self.map.accesibleTile(self.team1.buildings+self.team1.units+self.team2.buildings+self.team2.units)
    def gametick(self):

        self.goList = self.team1.buildings+self.team1.units+self.team2.buildings+self.team2.units+self.trees


        










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

        self.health = 10


    def _CreateWorker(x, y, team):

        return Worker(x, y, team)

    def _CreateScout(x, y, team):

        return Scout(x, y, team)


def main():

    np.set_printoptions(threshold=sys.maxsize)


