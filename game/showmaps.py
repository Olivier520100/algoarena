from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import cv2
from PIL import Image



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
        11: np.array([255,192,203]),
        12: np.array([41, 107, 42])
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


def getMapImageWithSprites(maps):
        
    terrainMap = maps[0]
    ressourceMap = maps[1]
    team1UnitMap = maps[2]
    team1BuildingMap = maps[3]
    team2UnitMap = maps[4]
    team2BuildingMap = maps[5]

    imagearray = np.zeros([terrainMap.shape[0]*10, terrainMap.shape[1]*10, 3])


    for currenty in range((terrainMap).shape[0]):
        for currentx in range((terrainMap).shape[1]):
            if terrainMap[currenty, currentx] in terrainsprites:
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = terrainsprites[terrainMap[currenty, currentx]]
            elif terrainMap[currenty, currentx] in terrain_colors:
                imagearray[currenty*10:currenty*10+10, currentx*10:currentx*10+10, :] = terrain_colors[terrainMap[currenty, currentx]]


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

def showImageList(mapList,gameID):

    image_list = []
    for frames in mapList:
        image_list.append(getMapImageWithSprites(frames))

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)
    image_display = plt.imshow(image_list[0], cmap='gray')
    plt.axis('off')

    def update(frame_index):
        image_display.set_data(image_list[int(frame_index)])
        fig.canvas.draw_idle()

    ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05]) 
    slider = Slider(ax=ax_slider, label='Frame', valmin=0, valmax=len(image_list) - 1, valinit=0, valfmt='%0.0f')

    slider.on_changed(update)

    plt.show()

        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_file = f'{gameID}.mov'
    frame_rate = 30 
    height, width, layers = image_list[0].shape
    video = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    for image in image_list:
        frame = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR)
        video.write(frame)

    video.release()

    print("Video saved as", output_file)

    

def showMap(terrainMap):
        


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

