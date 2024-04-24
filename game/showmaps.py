from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import cv2

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

def getMapImage(terrainMap):
        

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

    return (imagearray.astype('uint8'))

def showImageList(terrainMapList):

    image_list = []
    for frames in terrainMapList:
        image_list.append(getMapImage(frames))

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

    # plt.show()
    # expanded_image_list = []

    # for image in image_list:
    #     height, width = image.shape[:2]
    #     new_size = (width * 10, height * 10)  # Increase both dimensions by a factor of 10
    #     # Resize using nearest neighbor interpolation
    #     expanded_image = cv2.resize(image, new_size, interpolation=cv2.INTER_NEAREST)
    #     expanded_image_list.append(expanded_image)
        
    # fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # You can also use other codecs like 'XVID', 'MJPG'.
    # output_file = 'output_video.mp4'
    # frame_rate = 24  # Or whatever frame rate you want.
    # height, width, layers = expanded_image_list[0].shape  # Assumes all images have the same shape.
    # video = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    # # Add frames to the video.
    # for image in expanded_image_list:
    #     frame = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR)  # Convert RGB to BGR.
    #     video.write(frame)

    # # Release everything when job is finished.
    # video.release()

    # print("Video saved as", output_file)

    

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

