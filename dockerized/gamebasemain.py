import numpy as np

import pandas
import random
import numpy as np

import player1
import player2
import videogeneration
from player import Player


def nextPosition(startPosition, endPosition, availablePositionMatrix):
    ##Finds the next optimal position for the unit based on start, end and the available pos
    min_value = float('inf')
    next_pos = startPosition

    weightMatrix = dijkstra(startPosition, endPosition, availablePositionMatrix)
    
    if weightMatrix is not None:

        rows, cols = weightMatrix.shape
        directions = [(0,0),(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = startPosition[0] + dx, startPosition[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if weightMatrix[nx, ny] < min_value:
                    min_value = weightMatrix[nx, ny]
                    next_pos = [nx, ny]
        return next_pos
    else: 
        return startPosition
  
def dijkstra(startPosition, tempEndPosition, availablePositionMatrix):
    #Generates a heat map of closest tile to end pos
    maxval = 10000
    availablePositionMatrix[startPosition[0],startPosition[1]] = True
    weightMatrix = np.zeros(availablePositionMatrix.shape) + maxval
    cols, rows = weightMatrix.shape

    cardinallist = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cornerlist = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    cardinaladd = 1
    corneradd = 1.414

    if not (0 <= startPosition[0] < cols and 0 <= startPosition[1] < rows):
        return None
    if not(0 <= tempEndPosition[0] < cols and 0 <= tempEndPosition[1] < rows):
        return None



    if availablePositionMatrix[tempEndPosition[0],tempEndPosition[1]] == False:
        surroundset = {(tempEndPosition[0],tempEndPosition[1])}
        found = False
        while found == False:
            tempnextset = set()
            for coords in surroundset:
                ty, tx = coords[0], coords[1]
                for y,x in cardinallist:
                    nx = coords[1] + x
                    ny = coords[0] + y
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if availablePositionMatrix[ny,nx] == True:
                            endPosition = [ny,nx]
                            found = True
                            break
                        else:
                            tempnextset.add((ny,nx))
                if found:
                    break
                for y,x in cornerlist:
                    nx = coords[1] + x
                    ny = coords[0] + y
                    if 0 <= nx < rows and 0 <= ny < cols:

                        if availablePositionMatrix[ny,nx] == True:
                            endPosition = [ny,nx]
                            found = True
                            break
                        else: 
                            tempnextset.add((ny,nx))

                if found:
                    break
            surroundset=tempnextset
    else:
        endPosition = tempEndPosition
    weightMatrix[endPosition[0], endPosition[1]] = 0
    surroundset = set()

    for y,x in cardinallist:
        nx = endPosition[1] + x
        ny = endPosition[0] + y
        if 0 <= nx < rows and 0 <= ny < cols:

            if availablePositionMatrix[ny,nx] == True:  
                weightMatrix[ny,nx] = cardinaladd
                surroundset.add((ny,nx))
    for y,x in cornerlist:
        nx = endPosition[1] + x
        ny = endPosition[0] + y
        if 0 <= nx < rows and 0 <= ny < cols:

            if availablePositionMatrix[ny,nx] == True:
                weightMatrix[ny,nx] = corneradd
                surroundset.add((ny,nx))
    counter=1
    while weightMatrix[startPosition[0],startPosition[1]] == maxval and counter < 10000:
        tempnextset = set()
        counter+=1        
        for coords in surroundset:
            ty, tx = coords[0], coords[1]
            for y,x in cardinallist:
                nx = coords[1] + x
                ny = coords[0] + y
                if 0 <= nx < rows and 0 <= ny < cols:

                    if availablePositionMatrix[ny,nx] == True:
                        if weightMatrix[ny,nx] > weightMatrix[ty,tx] + cardinaladd:
                            weightMatrix[ny,nx] = weightMatrix[ty,tx] + cardinaladd
                            tempnextset.add((ny,nx))
            for y,x in cornerlist:
                nx = coords[1] + x
                ny = coords[0] + y
                if 0 <= nx < rows and 0 <= ny < cols:

                    if availablePositionMatrix[ny,nx] == True:
                        if weightMatrix[ny,nx] > weightMatrix[ty,tx] + corneradd:
                            weightMatrix[ny,nx] = weightMatrix[ty,tx] + corneradd
                            tempnextset.add((ny,nx))
                
        surroundset = tempnextset

    
    return weightMatrix
def coordinatesRange(range):
    #Generates adjacent tiles for a given range
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T
    

#Class that contains most game logic

class Game():

    def __init__(self):

        #inititalize game logic and base max turns, current turn, the list of all the frames that will be used to generate the video and the player objects
        self.gameOutcome = (1,1)
        self.maxturns = 10
        self.turn = 0 
        self.frames = []
        self.player1 = Player()
        self.player2 = Player()


        #Chooses the map
        a = pandas.read_csv("maps.csv")
        mapnumber = 2
        self.terrainMap = np.load(a["Filename"].iloc[mapnumber-1])
        filename = a["Filename"].iloc[mapnumber-1]
        self.terrainMap = np.load(filename)

        #Initializes base game info of the map
        self.mapsizey = (self.terrainMap).shape[0]
        self.mapsizex = (self.terrainMap).shape[1]

        self.team1startcoords = [a['Team1Starty'].iloc[mapnumber-1], a['Team1Startx'].iloc[mapnumber-1]]
        self.team2startcoords = [a['Team2Starty'].iloc[mapnumber-1], a['Team2Startx'].iloc[mapnumber-1]]

        self.walkableMapCreation(self.team1startcoords)
        self.waterMapCreation()
        self.mineableMapCreation()


        #Creates trees and player objects
        self.team1 = Team(self.team1startcoords)
        self.team2 = Team(self.team2startcoords)

        self.treeGeneration()
    
    def gameRun(self, gameId, maxturn):

        # Runs the simulation of everyturn
        self.maxturns = maxturn
        
        print("Started Simulation")


        while self.turn < self.maxturns:

            # print("Turn: ", self.turn)

            self.goListCreation()
            self.accesibleMapCreation()
            self.updatePlayerInfo()
            self.updateMaps()
            self.frames.append([self.terrainMap,self.ressourceMap,self.team1UnitMap,self.team1BuildingMap,self.team2UnitMap,self.team2BuildingMap])

            if self.gameOutcome[0] + self.gameOutcome[1] < 2:
                break
            self.processRequest()
            self.runAction()
            
            self.turn +=1
            
        print("Finished Simulation")
        #Sends info to the video generations
        videogeneration.generateVideo(self.frames, gameId)    
        #Returns the game outcome
        if self.turn == self.maxturns:
            if self.team1.buildings[0].health > self.team2.buildings[0].health:
                return (1,0)
            elif self.team1.buildings[0].health < self.team2.buildings[0].health:
                return(0,1)
            else:
                return (1,1)
        
        else: 

            return self.gameOutcome

          
    def updatePlayerInfo(self):

        ## Updates what info the user can read in the from the player class in the player1/2.py
        self.player1.reset()
        for units in self.team1.units:
            
            if issubclass(units.goal.__class__,GameObject):
                goal = {
                    "type": units.goal.__class__.__name__,
                    "health": units.goal.health,
                    "coordinates": units.goal.coordinates
                }
            else: 
                goal = units.goal

            self.player1.myUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates,
                    "goal": goal
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
        self.team1.summonCoordUpdate(self.accesibleTiles)
        self.player1.summoncoords = self.team1.summoncoords
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
            if issubclass(units.goal.__class__,GameObject):
                goal = {
                    "type": units.goal.__class__.__name__,
                    "health": units.goal.health,
                    "coordinates": units.goal.coordinates
                }
            else: 
                goal = units.goal
            self.player2.myUnits.append(
                {
                    "type": units.__class__.__name__,
                    "health": units.health,
                    "coordinates": units.coordinates,
                    "goal": goal

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
        self.team2.summonCoordUpdate(self.accesibleTiles)
        self.player2.summoncoords = self.team2.summoncoords

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
        for trees in self.trees:
            self.player1.trees.append({
                "type": trees.__class__.__name__,
                "health": trees.health,
                "coordinates": trees.coordinates
            })
            self.player2.trees.append({
                "type": trees.__class__.__name__,
                "health": trees.health,
                "coordinates": trees.coordinates
            })
    def walkableMapCreation(self,initialtile):

        #finds what area is walkable using modified djstras algorithm
        walkableTerrainTemp = (self.terrainMap == 2) | (self.terrainMap == 3) | (self.terrainMap == 4) | (self.terrainMap == 9)
        self.walkableTerrain = np.zeros([self.mapsizey, self.mapsizex]) == 1
        self.walkableTerrain[initialtile[0],initialtile[1]] = True
        
        surroundset = set()

        cardinallist = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for y,x in cardinallist:

            
            nx = initialtile[1] + x
            ny = initialtile[0] + y

            if 0 < ny < self.mapsizey and 0 <nx < self.mapsizex:

                if walkableTerrainTemp[ny,nx] == True and nx < self.mapsizex and ny < self.mapsizey:
                    self.walkableTerrain[ny,nx] = True
                    surroundset.add((ny,nx))

        while len(surroundset)> 0:
            tempnextset = set()
                   
            for coords in surroundset:
                
                for y,x in cardinallist:
                    nx = coords[1] + x
                    ny = coords[0] + y

                    if 0< ny < self.mapsizey and 0< nx < self.mapsizex:

                        if walkableTerrainTemp[ny,nx] == True and nx < self.mapsizex and ny < self.mapsizey and not self.walkableTerrain[ny,nx]:
                            self.walkableTerrain[ny,nx] = True
                            tempnextset.add((ny,nx))
            surroundset = tempnextset
    def waterMapCreation(self):
        self.waterTerrain = (self.terrainMap == 1)
    def mineableMapCreation(self):
        self.rockTerrain = (self.terrainMap == 5) | (self.terrainMap == 6) | (self.terrainMap == 7) | (self.terrainMap == 8)
    def goListCreation(self):
        #Creates a list of all the game objects
        self.goList = self.team1.buildings+self.team1.units+self.trees+self.team2.buildings+self.team2.units
    def accesibleMapCreation(self):
        #finds what is accessbile by foot 
        self.unitTruth = np.zeros([self.mapsizey, self.mapsizex]) == 0
        for go in self.goList:
            if issubclass(go.__class__,Building):
                coordinates = coordinatesRange(go.rad) + np.array(go.coordinates)
                for coordinate in coordinates:
                    if 0 <= coordinate[0] and coordinate[0] < self.mapsizey and 0 <= coordinate[1] and coordinate[1] < self.mapsizex:
                        self.unitTruth[int(coordinate[0]),int(coordinate[1])] = False
            else: 
                if 0 <= go.coordinates[0] and go.coordinates[0] < self.mapsizey and 0 <= go.coordinates[1] and go.coordinates[1] < self.mapsizex:

                    self.unitTruth[go.coordinates[0] , go.coordinates[1]] = False

        self.accesibleTiles = np.logical_and(self.unitTruth,self.walkableTerrain)
    def treeGeneration(self):
        #generates trees with certain range around so none too close
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

        maxtree = 10000
        treecount = 0
        maxiterations = 100000
        treerad = 1
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
    def processRequest(self):
        
        ## Processes the requests for each player
        self.updatePlayerInfo()
        requestPlayer1 = player1.playerAction(self.player1)
        requestPlayer2 = player2.playerAction(self.player2)
        unitTypes = {"Worker", "Melee", "Archer", "Tank", "GlassCannon"}
        buildingType = {"Castle"}
        ressourceType = {"Tree"}
        if not requestPlayer1.gameObjectDict == None:
            if requestPlayer1.gameObjectDict["type"] in unitTypes:
                unitindex = -1
                listindex = 0
                for units in self.player1.myUnits:
                    if units == requestPlayer1.gameObjectDict:
                        unitindex = listindex
                        break
                    listindex+=1
                if len(requestPlayer1.gameRequestDict) == 1 and "coordinates" in requestPlayer1.gameRequestDict:
                    if unitindex != -1:
                        self.team1.units[unitindex].goal = requestPlayer1.gameRequestDict["coordinates"]
                elif requestPlayer1.gameRequestDict["type"] in ressourceType: 
                    
                    treeindex = -1
                    listindex = 0
                    for tree in self.player1.trees:
                        if tree == requestPlayer1.gameRequestDict:
                            treeindex = listindex
                            break
                        listindex+=1
                    if unitindex != -1 and treeindex != -1:
                        self.team1.units[unitindex].goal = self.trees[treeindex]
                        self.trees[treeindex].goalof.append(self.team1.units[unitindex])

                elif requestPlayer1.gameRequestDict["type"] in unitTypes: 
                    enemyunit = -1
                    listindex = 0
                    for unit in self.player1.enemyUnits:
                        if unit == requestPlayer1.gameRequestDict:
                            enemyunit = listindex
                            break
                        listindex+=1

                    if unitindex != -1 and enemyunit != -1:
                        self.team1.units[unitindex].goal = self.team2.units[enemyunit]
                        self.team2.units[enemyunit].goalof.append(self.team1.units[unitindex])

                
                elif requestPlayer1.gameRequestDict["type"] in buildingType: 
                    buildingIndex = -1
                    listindex = 0
                    for unit in self.player1.enemyBuildings:
                        if unit == requestPlayer1.gameRequestDict:
                            buildingIndex = listindex
                            break
                        listindex+=1
                    if unitindex != -1 and buildingIndex != -1:
                        self.team1.units[unitindex].goal = self.team2.buildings[buildingIndex]
                        self.team2.buildings[buildingIndex].goalof.append(self.team1.units[unitindex])

            elif requestPlayer1.gameObjectDict["type"] in buildingType:
                index = -1
                listindex = 0
                for units in self.player1.myUnits:
                    if units == requestPlayer1.gameRequestDict:
                        index = listindex
                        break
                    listindex+=1
                if index == -1:
                    if "health" not in requestPlayer1.gameRequestDict:
                        self.team1.summonUnit(requestPlayer1.gameRequestDict["coordinates"],requestPlayer1.gameRequestDict["type"])
                   
        if not requestPlayer2.gameObjectDict == None:
            if requestPlayer2.gameObjectDict["type"] in unitTypes:
                unitindex = -1
                listindex = 0
                for units in self.player2.myUnits:
                    if units == requestPlayer2.gameObjectDict:
                        unitindex = listindex
                        break
                    listindex+=1
                if len(requestPlayer2.gameRequestDict) == 1 and "coordinates" in requestPlayer2.gameRequestDict:
                    if unitindex != -1:
                        self.team2.units[unitindex].goal = requestPlayer2.gameRequestDict["coordinates"]
                elif requestPlayer2.gameRequestDict["type"] in ressourceType: 
                    treeindex = -1
                    listindex = 0
                    for tree in self.player2.trees:
                        if tree == requestPlayer2.gameRequestDict:
                            treeindex = listindex
                            break
                        listindex+=1
                    if unitindex != -1 and treeindex != -1:
                        self.team2.units[unitindex].goal = self.trees[treeindex]
                        self.trees[treeindex].goalof.append(self.team2.units[unitindex])

                elif requestPlayer2.gameRequestDict["type"] in unitTypes: 
                    enemyunit = -1
                    listindex = 0
                    for unit in self.player2.enemyUnits:
                        if unit == requestPlayer2.gameRequestDict:
                            enemyunit = listindex
                            break
                        listindex+=1

                    if unitindex != -1 and enemyunit != -1:
                        self.team2.units[unitindex].goal = self.team1.units[enemyunit]
                        self.team1.units[enemyunit].goalof.append(self.team2.units[unitindex])

                elif requestPlayer2.gameRequestDict["type"] in buildingType: 
                    buildingIndex = -1
                    listindex = 0
                    for unit in self.player2.enemyBuildings:
                        if unit == requestPlayer2.gameRequestDict:
                            buildingIndex = listindex
                            break
                        listindex+=1
                    if unitindex != -1 and buildingIndex != -1:
                        self.team2.units[unitindex].goal = self.team1.buildings[buildingIndex]
                        self.team1.buildings[buildingIndex].goalof.append(self.team2.units[unitindex])

            elif requestPlayer2.gameObjectDict["type"] in buildingType:
                index = -1
                listindex = 0
                for units in self.player2.myUnits:
                    if units == requestPlayer2.gameRequestDict:
                        index = listindex
                        break
                    listindex+=1
                if index == -1:
                    if "health" not in requestPlayer2.gameRequestDict:
                        self.team2.summonUnit(requestPlayer2.gameRequestDict["coordinates"],requestPlayer2.gameRequestDict["type"])
    def runAction(self):

        ##runs the actions for each team alternating
        self.accesibleMapCreation()
        self.unitActionKill(self.trees)
        self.gameOutcome = (self.team1.deathCheck(),self.team2.deathCheck())
        if self.turn % 2 == 0:
            self.accesibleMapCreation()
            self.unitActionKill(self.team1.units)
            self.unitActionKill(self.team2.units)

        else: 
            self.accesibleMapCreation()
            self.unitActionKill(self.team2.units)
            self.unitActionKill(self.team1.units)
    def unitActionKill(self,listToRemove: list):
        #destroyts units that arent alive
        indextoremove = []
        index = 0
        for units in listToRemove:
            if units.health > 0:
                units.action(self.accesibleTiles)
            else:
                indextoremove.append(index)
            index+=1
        indextoremove.reverse()

        try:
            for index in indextoremove:
                listToRemove.pop(index)
        except:
            print(indextoremove)

    def updateMaps(self):

        ##Updates the maps for the graphics
                
        self.ressourceMap = np.zeros([self.mapsizey, self.mapsizex])

        for trees in self.trees:
            self.ressourceMap[trees.coordinates[0],trees.coordinates[1]] = 1

        self.team1UnitMap = np.zeros([self.mapsizey, self.mapsizex])

        for unit in self.team1.units:
            if issubclass(unit.__class__,Worker):
                self.team1UnitMap[unit.coordinates[0], unit.coordinates[1]] = 1
            elif issubclass(unit.__class__,Melee):
                self.team1UnitMap[unit.coordinates[0], unit.coordinates[1]] = 2
            elif issubclass(unit.__class__,Tank):
                self.team1UnitMap[unit.coordinates[0], unit.coordinates[1]] = 3
            elif issubclass(unit.__class__,Archer):
                self.team1UnitMap[unit.coordinates[0], unit.coordinates[1]] = 4
            elif issubclass(unit.__class__,GlassCannon):
                self.team1UnitMap[unit.coordinates[0], unit.coordinates[1]] = 5

        self.team1BuildingMap = np.zeros([self.mapsizey, self.mapsizex])

        for building in self.team1.buildings:
            self.team1BuildingMap[building.coordinates[0]-building.rad, building.coordinates[1]-building.rad] = 1

        self.team2UnitMap = np.zeros([self.mapsizey, self.mapsizex])

        for unit in self.team2.units:
            if issubclass(unit.__class__,Worker):
                self.team2UnitMap[unit.coordinates[0], unit.coordinates[1]] = 1
            elif issubclass(unit.__class__,Melee):
                self.team2UnitMap[unit.coordinates[0], unit.coordinates[1]] = 2
            elif issubclass(unit.__class__,Tank):
                self.team2UnitMap[unit.coordinates[0], unit.coordinates[1]] = 3
            elif issubclass(unit.__class__,Archer):
                self.team2UnitMap[unit.coordinates[0], unit.coordinates[1]] = 4
            elif issubclass(unit.__class__,GlassCannon):
                self.team2UnitMap[unit.coordinates[0], unit.coordinates[1]] = 5

        self.team2BuildingMap = np.zeros([self.mapsizey, self.mapsizex])

        for building in self.team2.buildings:
            self.team2BuildingMap[building.coordinates[0]-building.rad, building.coordinates[1]-building.rad] = 1
                

## Team class
class Team():

    def __init__(self,coordinates):

        ##defines base units

        self.units = []

        self.buildings = []

        self.wood = 100

        self.stone = 100

        self.buildings.append(Castle(coordinates))

        self.mainBuilding =  self.buildings[0]

        self.summoncoords = []

    def summonCoordUpdate(self,availablecoords):

        #generates possible summoning coords to the player class to erceive
        
        summonradcoords = set()
        buildingunitcoords = set()
        self.summoncoords = []

        for building in self.buildings:

            tempsummonradarray = coordinatesRange(building.sumrad) + building.coordinates
            tempbuildingradarray  = coordinatesRange(building.rad) + building.coordinates
            tempsummonset = set(map(tuple,tempsummonradarray))
            tempbuildingset = set(map(tuple,tempbuildingradarray))
            summonradcoords= summonradcoords | (tempsummonset)
            buildingunitcoords = buildingunitcoords | (tempbuildingset)

        tempsummoncoords = summonradcoords - buildingunitcoords
        
        for coordinates in tempsummoncoords:
            if availablecoords[int(coordinates[0]),int(coordinates[1])] == True:
                self.summoncoords.append([int(coordinates[0]),int(coordinates[1])])
    def summonUnit(self, coords, type):

        #function to call summon a unit

        matches = np.all(np.array(self.summoncoords) == np.array(coords), axis=1)
        exists = np.any(matches)
        if exists:
            if type == "Worker" and self.wood >= 20:
                self.units.append(Worker(coords,self))
                self.wood -= 20
            if type == "Melee" and self.wood >= 30:
                self.units.append(Melee(coords,self))
                self.wood -= 30
            if type == "Tank" and self.wood >= 70:
                self.units.append(Tank(coords,self))
                self.wood -= 70
            if type == "Archer" and self.wood >= 80:
                self.units.append(Archer(coords,self))
                self.wood -= 70
            if type == "GlassCannon" and self.wood >= 90:
                self.units.append(GlassCannon(coords,self))
                self.wood -= 70
    def deathCheck(self):
        #verify if dead
        if self.mainBuilding.health <= 0:
            return 0
        else:
            return 1
        

#generates gameobject class

class GameObject(): 

    def __init__(self, coordinates):

        #initializes base info

        self.possible_actions = set()

        self.health = 10

        self.coordinates = coordinates

        self.goalof = []

        self.goal = None

    def deathCheck(self):
    
        if self.health <= 0:
            for target in self.goalof:
                target.goal = None


    def action(self,availableposition):
        pass

class Tree(GameObject):

    def __init__(self, coordinates):

        super().__init__(coordinates)

        self.health = 10

class Units(GameObject):

    def __init__(self, coordinates, team):

        super().__init__(coordinates)

        self.team = team

        self.canAttack = True

        self.canGather = True

        self.damage = 1

        self.gather = 1

        self.speed = 0

        self.speedcounter = 0

        self.cooldown = 0

        self.cooldowncounter = 0

        self.range = 1
        
    def action(self,availableposition):
        #all actions, gather move and attack.
        if type(self.goal) == list and len(self.goal) == 2:

            if self.speedcounter == 0:
                if self.coordinates != self.goal:
                    nextpos = nextPosition(self.coordinates,self.goal,availableposition)
                    if nextpos == self.coordinates:
                        self.goal = None
                    else: 
                        self.coordinates = nextpos
                else:
                    self.goal = None
                
                self.speedcounter+=1
            else: 
                if self.speedcounter >= self.speed:
                    self.speedcounter=0
                else:
                    self.speedcounter+=1
            
        elif issubclass(self.goal.__class__,Units):
            adjacentcoordinates = coordinatesRange(self.range)+ self.coordinates
            matches = np.all(np.array(adjacentcoordinates) == np.array(self.goal.coordinates), axis=1)
            exists = np.any(matches)

            if exists:
                self.goal.health-=self.damage
                self.goal.deathCheck()
            else:
                if self.speedcounter == 0:
                    nextpos = nextPosition(self.coordinates,self.goal.coordinates,availableposition)
                    if nextpos == self.coordinates:
                        self.goal = None
                    else: 
                        self.coordinates = nextpos
                
                    self.speedcounter+=1
                else: 
                    if self.speedcounter >= self.speed:
                        self.speedcounter=0
                    else:
                        self.speedcounter+=1

        elif issubclass(self.goal.__class__,Tree):

            adjacentcoordinates = coordinatesRange(self.range)+ self.coordinates
            matches = np.all(np.array(adjacentcoordinates) == np.array(self.goal.coordinates), axis=1)
            exists = np.any(matches)

            if exists:
                self.goal.health-=self.gather
                self.team.wood += 1
                self.goal.deathCheck()
            else:
                if self.speedcounter == 0:
                    nextpos = nextPosition(self.coordinates,self.goal.coordinates,availableposition)
                    if nextpos == self.coordinates:
                        self.goal = None
                    else: 
                        self.coordinates = nextpos
                
                    self.speedcounter+=1
                else: 
                    if self.speedcounter >= self.speed:
                        self.speedcounter=0
                    else:
                        self.speedcounter+=1

        elif issubclass(self.goal.__class__,Building):

            adjacentcoordinates = coordinatesRange(self.range)+ self.coordinates
            buildingcoordinates = coordinatesRange(self.goal.rad)+ self.goal.coordinates
            matches = False
            for buildingcoords in buildingcoordinates:
                matches = np.all(np.array(adjacentcoordinates) == np.array(buildingcoords), axis=1)
                exists = np.any(matches)
                if exists:
                    break

            if exists:
                self.goal.health-=self.damage
            else:
                if self.speedcounter == 0:
                    nextpos = nextPosition(self.coordinates,self.goal.coordinates,availableposition)
                    if nextpos == self.coordinates:
                        self.goal = None
                    else: 
                        self.coordinates = nextpos
                
                    self.speedcounter+=1
                else: 
                    if self.speedcounter >= self.speed:
                        self.speedcounter=0
                    else:
                        self.speedcounter+=1

#game object classes etc
    
class UtilityUnits(Units):

    def __init__(self, coordinates, team):

        super().__init__(coordinates, team)

class Worker(UtilityUnits):

    def __init__(self, coordinates,team):

        super().__init__(coordinates,team)

        self.coordinates = coordinates

        self.health = 15

        self.damage = 0

        self.gather = 2

        self.speed = 1

        self.speedcounter = 0

        self.cooldown = 1

        self.cooldowncounter = 0

        self.range = 1

class CombatUnits(Units):

    def __init__(self, coordinates, team):

        super().__init__(coordinates, team)

class Melee(CombatUnits):

    def __init__(self, coordinates,team):

        super().__init__(coordinates,team)

        self.coordinates = coordinates

        self.health = 20

        self.damage = 4

        self.gather = 0

        self.speed = 2

        self.speedcounter = 0

        self.cooldown = 2

        self.cooldowncounter = 0

        self.range = 1

class Tank(CombatUnits):

    def __init__(self, coordinates,team):

        super().__init__(coordinates,team)

        self.coordinates = coordinates

        self.health = 30

        self.damage = 2

        self.gather = 0

        self.speed = 4

        self.speedcounter = 0

        self.cooldown = 3

        self.cooldowncounter = 0

        self.range = 1

class Archer(CombatUnits):

    def __init__(self, coordinates,team):

        super().__init__(coordinates,team)

        self.coordinates = coordinates

        self.health = 7

        self.damage = 2

        self.gather = 0

        self.speed = 3

        self.speedcounter = 0

        self.cooldown = 2

        self.cooldowncounter = 0

        self.range = 5

class GlassCannon(CombatUnits):

    def __init__(self, coordinates,team):

        super().__init__(coordinates,team)

        self.coordinates = coordinates

        self.health = 3

        self.damage = 5

        self.gather = 0

        self.speed = 1

        self.speedcounter = 0

        self.cooldown = 2

        self.cooldowncounter = 0

        self.range = 1

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
        self.health = 100



