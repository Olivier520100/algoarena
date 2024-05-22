import math
import numpy as np
import cv2
from PIL import Image
import random


## BASE COLORS AND SPRITE LOCATIONS

terrain_colors = {
        0: np.array([0, 0, 0]),          # fog
        1: np.array([0, 0, 255]),        # water
        2: np.array([255, 255, 0]),      # sand
        3: np.array([50, 237, 53]),        # grass1
        4: np.array([50, 237, 53]),        # grass2
        5: np.array([128, 128, 128]),    # stone1
        6: np.array([160, 160, 160]),    # stone2
        7: np.array([180, 180, 180]),    # stone3
        8: np.array([200, 200, 200]),    # stone4
        9: np.array([143, 101, 0]),       # bridge
        10: np.array([255,0,0]), #team1
        11: np.array([118,66,138]), #team 2
        12: np.array([41, 107, 42]) # tree
    }

terrainsprites = {

    1: np.asarray(Image.open("assets/terrain/water.png"))[:,:,:3],
    2: np.asarray(Image.open("assets/terrain/sand.png"))[:,:,:3],
    3: np.asarray(Image.open("assets/terrain/grass.png"))[:,:,:3],
    4: np.asarray(Image.open("assets/terrain/grass2.png"))[:,:,:3],
    5: np.asarray(Image.open("assets/terrain/rock0.png"))[:,:,:3],
    6: np.asarray(Image.open("assets/terrain/rock1.png"))[:,:,:3],
    7: np.asarray(Image.open("assets/terrain/rock2.png"))[:,:,:3],
    8: np.asarray(Image.open("assets/terrain/rock3.png"))[:,:,:3],
    9: np.asarray(Image.open("assets/terrain/bridge.png"))[:,:,:3],

}

ressourcesprites = {
    1: np.asarray(Image.open("assets/ressources/tree.png"))
}

team1unitsprites = {
    1: np.asarray(Image.open("assets/units/unit-w-1.png")),
    2: np.asarray(Image.open("assets/units/unit-m-1.png")),
    3: np.asarray(Image.open("assets/units/unit-t-1.png")),
    4: np.asarray(Image.open("assets/units/unit-a-1.png")),
    5: np.asarray(Image.open("assets/units/unit-gc-1.png")),


}
team1buildingsprites = {
    1: np.asarray(Image.open("assets/buildings/castle-1.png")),

}
team2unitsprites = {
    1: np.asarray(Image.open("assets/units/unit-w-2.png")),
    2: np.asarray(Image.open("assets/units/unit-m-2.png")),
    3: np.asarray(Image.open("assets/units/unit-t-2.png")),
    4: np.asarray(Image.open("assets/units/unit-a-2.png")),
    5: np.asarray(Image.open("assets/units/unit-gc-2.png")),


}
team2buildingsprites = {
    1: np.asarray(Image.open("assets/buildings/castle-2.png")),
}

def getMapImageWithSprites(maps):

    ##GENERATES IMAGES OF EACH FRAME WITH SPRITES
        
    terrainMap = maps[0]
    ressourceMap = maps[1]
    team1UnitMap = maps[2]
    team1BuildingMap = maps[3]
    team2UnitMap = maps[4]
    team2BuildingMap = maps[5]

    imagearray = np.zeros([terrainMap.shape[0]*10, terrainMap.shape[1]*10, 3])

    #CREATES BASE LAYERS WITH TERRAIN SPRITES

    for currenty in range((terrainMap).shape[0]):
        for currentx in range((terrainMap).shape[1]):
            if terrainMap[currenty, currentx] in terrainsprites:
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = terrainsprites[terrainMap[currenty, currentx]]

    #Adds trees, units sprites over the terrain

    for currenty in range((terrainMap).shape[0]):
        for currentx in range((terrainMap).shape[1]):


            if ressourceMap[currenty, currentx] in ressourcesprites:
                background = imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :]
                sprite = ressourcesprites[ressourceMap[currenty, currentx]]
                
                for i in range(10):
                    for j in range(10): 
                        if sprite[i,j,3] != 0:
                            background[i,j,:] = [0,0,0]
                result = sprite[:,:,:3]+background
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = result

            if team1UnitMap[currenty, currentx] in team1unitsprites:
                background = imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :]
                sprite = team1unitsprites[team1UnitMap[currenty, currentx]]
                for i in range(10):
                    for j in range(10): 
                        if sprite[i,j,3] != 0:
                            background[i,j,:] = [0,0,0]
                result = sprite[:,:,:3]+background
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = result

            if team1BuildingMap[currenty, currentx] in team1buildingsprites:
                background = imagearray[currenty*10:currenty*10+team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[0], currentx*10:currentx*10+team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[1], :]
                sprite = team1buildingsprites[team1BuildingMap[currenty, currentx]]
                for i in range(team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[0]):
                    for j in range(team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[1]): 
                        if sprite[i,j,3] != 0:
                            background[i,j,:] = [0,0,0]
                result = sprite[:,:,:3]+background
                imagearray[currenty*10:currenty*10+team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[0], currentx*10:currentx*10+team1buildingsprites[team1BuildingMap[currenty, currentx]].shape[1], :] = result

            if team2UnitMap[currenty, currentx] in team2unitsprites:
                background = imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :]
                sprite = team2unitsprites[team2UnitMap[currenty, currentx]]
                for i in range(10):
                    for j in range(10): 
                        if sprite[i,j,3] != 0:
                            background[i,j,:] = [0,0,0]
                result = sprite[:,:,:3]+background
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = result

            if team2BuildingMap[currenty, currentx] in team2buildingsprites:
                background = imagearray[currenty*10:currenty*10+team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[0], currentx*10:currentx*10+team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[1], :]
                sprite = team2buildingsprites[team2BuildingMap[currenty, currentx]]
                for i in range(team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[0]):
                    for j in range(team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[1]): 
                        if sprite[i,j,3] != 0:
                            background[i,j,:] = [0,0,0]
                result = sprite[:,:,:3]+background
                imagearray[currenty*10:currenty*10+team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[0], currentx*10:currentx*10+team2buildingsprites[team2BuildingMap[currenty, currentx]].shape[1], :] = result

    return (imagearray.astype('uint8'))



def getMapSimpleColors(maps):

    #Generates with simple colors
        
    terrainMap = maps[0]
    ressourceMap = maps[1]
    team1UnitMap = maps[2]
    team1BuildingMap = maps[3]
    team2UnitMap = maps[4]
    team2BuildingMap = maps[5]

    imagearray = np.zeros([terrainMap.shape[0], terrainMap.shape[1], 3])


    for currenty in range((terrainMap).shape[0]):
        for currentx in range((terrainMap).shape[1]):
            if terrainMap[currenty, currentx] in terrain_colors:
                imagearray[currenty, currentx, :] = terrain_colors[terrainMap[currenty, currentx]]


    for currenty in range((terrainMap).shape[0]):
        for currentx in range((terrainMap).shape[1]):

            if ressourceMap[currenty, currentx] in ressourcesprites:
                imagearray[currenty, currentx, :] = terrain_colors[12]

            if team1UnitMap[currenty, currentx] in team1unitsprites:
                imagearray[currenty, currentx, :] = terrain_colors[10]

            if team1BuildingMap[currenty, currentx] in team1buildingsprites:
                imagearray[currenty:currenty+7, currentx:currentx+7, :] = terrain_colors[10]

            if team2UnitMap[currenty, currentx] in team2unitsprites:
                imagearray[currenty, currentx, :] = terrain_colors[11]


            if team2BuildingMap[currenty, currentx] in team2buildingsprites:
                imagearray[currenty:currenty+7, currentx:currentx+7, :] = terrain_colors[11]

    return (imagearray.astype('uint8'))

def upscale(imageList, upscalefactor):

    #Upscales the image
    newImageList = []
    for image in imageList:
        upscaled_image = np.repeat(np.repeat(image, upscalefactor, axis=0), upscalefactor, axis=1)
        newImageList.append(upscaled_image)
    return newImageList

def zoomedInGeneration(gameStates, zoomlen, zoomsize, unZoomedImages, minimap):

    #Generates the zoomed based on decayed most movement of that frame

    decaylist = []

    #Calcultes movmenet of that frame
    for state in gameStates:

        team1UnitMap = state[2]
        team2UnitMap = state[4]
        combinedMap = team1UnitMap + team2UnitMap

        combinedMap[combinedMap != 0] = 1

        if decaylist:
            combinedMap = (decaylist[-1] -0.1) + combinedMap
            combinedMap = np.clip(combinedMap, 0, 1)
        
        decaylist.append(combinedMap)

    concactlist = []
    index = 0

    ## Combines for the frame length
    while index < len(decaylist):

        lowindex = index
        highindex = min((index+zoomlen),len(decaylist))
        concactlist.append(np.sum(np.stack(decaylist[lowindex:highindex]),axis=0))
        index+=zoomlen


    camheight = zoomsize[0]
    camwidth = zoomsize[1]
    currenty = 0
    currentx = 0
    bestpos = []

    #finds the best frame using a sliding window

    for state in concactlist:
        greatestsum = 0
        greatestcord = [-1,-1]
        currenty = 0
        currentx = 0
        while camheight+currenty < concactlist[0].shape[0] and camwidth+currentx < concactlist[0].shape[1]:
            lowy = currenty
            highy = currenty+camheight
            lowx = currentx
            highx = currentx+camwidth
            
            currentsum = np.sum(state[lowy:highy, lowx:highx])
            if currentsum > greatestsum:
                greatestsum = currentsum
                greatestcord = [currenty,currentx]
            
            currentx+=1
            if camwidth+currentx >= concactlist[0].shape[1]:
                currenty+=1
                currentx=0
        bestpos.append(greatestcord)

    # Zooms in on main map
    resultImageList = []
    index = 0

    for images in unZoomedImages:
        bestposcounter = math.floor(index/zoomlen)
        lowy = bestpos[bestposcounter][0]*10
        highy = lowy+camheight*10
        lowx = bestpos[bestposcounter][1]*10
        highx =lowx+camwidth*10
        resultImageList.append(images[lowy:highy, lowx:highx])
        index+=1

    newminimap = []
    
    ## adding frame to minimap
    index = 0
    for images in minimap:

        
        bestposcounter = math.floor(index/zoomlen)
        lowy = bestpos[bestposcounter][0]
        highy = lowy+camheight
        lowx = bestpos[bestposcounter][1]
        highx =lowx+camwidth
        images[lowy:highy,lowx,:] = [0,0,0]
        images[lowy:highy,highx,:] = [0,0,0]
        images[lowy,lowx:highx,:] = [0,0,0]
        images[highy,lowx:highx,:] = [0,0,0]
    
        newminimap.append(images)
        index+=1

    
    return resultImageList, newminimap




def generateVideo(gameStates,gameID):


    ## Generating video components

    ## Time for each zoom
    zoomlen = 24*8

    ## Area zoom 
    zoomsize = [18,32]

    #Zoomed states

    unZoomedImages = []
    zoomedImages = []
    minimap = []

    #Generating images
    print("Generating")

    for frames in gameStates:
        unZoomedImages.append(getMapImageWithSprites(frames))
        minimap.append(getMapSimpleColors(frames))
    ##Zooming 

    print("Zooming")

    zoomedImages, minimapframed = zoomedInGeneration(gameStates,zoomlen,zoomsize,unZoomedImages,minimap)

    print("Scaling")

    zoomedImages = upscale(zoomedImages,4)
    unZoomedImages = upscale(unZoomedImages,2)
    minimap = upscale(minimap,2)
    minimapframed = upscale(minimapframed,2)

    print("Editing")


    zoomlist = [False]

    zoomtimers = math.ceil(len(unZoomedImages)/zoomlen)
    while len(zoomlist) < zoomtimers - 1:
        if random.randint(0, 1) == 1:
            zoomlist.append(True)
            if len(zoomlist) < zoomtimers - 1:
                zoomlist.append(False)
        else:
            zoomlist.append(False)

    zoomlist.append(False)


    print(zoomedImages[0].shape, unZoomedImages[0].shape, minimapframed[0].shape, minimap[0].shape)

    coordinatezoomedin = [int((unZoomedImages[0].shape[0] - zoomedImages[0].shape[0])/2),int((unZoomedImages[0].shape[1] - zoomedImages[0].shape[1])/2)]
    index = 0
    videosegments = []
    print(zoomlist)
    mainborder = 5

    while index < len(zoomedImages):
        

        newimage = unZoomedImages[index]
        bestposcounter = math.floor(index/zoomlen)

        if zoomlist[bestposcounter] == True:
            lowy = coordinatezoomedin[0]
            lowx = coordinatezoomedin[1]
            highy = lowy+zoomedImages[index].shape[0]
            highx = lowx+zoomedImages[index].shape[1]
            newimage[lowy-mainborder:highy+mainborder, lowx-mainborder:highx+mainborder, :] = [0,0,0]
            newimage[lowy:highy, lowx:highx, :] = zoomedImages[index]

        videosegments.append(newimage)
        index+=1

        




    print("Creating Video")


    fourcc = cv2.VideoWriter_fourcc(*'HVEC')
    output_file = f'videos/{gameID}.mp4'
    
    
    
    frame_rate = 24

    # image_list = upscale(framelist,2)
    height, width, layers = videosegments[0].shape

    video = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    for image in videosegments:
        frame = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR)
        video.write(frame)

    video.release()

    print("Video saved as", output_file)



    