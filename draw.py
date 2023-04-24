import json
import random
import sys
from typing import List
import jsonpickle
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import time
from APIResponse import FeatureType, Room, Wall
from config import CONFIG

def draw(junctions,wallsobj:List[Wall],rooms:List[Room]):
    xmin = 99999999999
    xmax = 0
    ymin = 99999999999
    ymax = 0

    for wall in wallsobj:
        if xmin > wall.fromPosition.x:
            xmin = wall.fromPosition.x
        if xmax < wall.toPosition.x:
            xmax = wall.toPosition.x
        if ymin > wall.fromPosition.y:
            ymin = wall.fromPosition.y
        if ymax < wall.toPosition.y:
            ymax = wall.toPosition.y

    w = xmax - xmin + 200
    h = ymax - ymin + 200
    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
    img1 = ImageDraw.Draw(im)

    wall_width = 10
    wall_width_half = wall_width/2

    for room in rooms:
        r = lambda: random.randint(0,255)
        fill = f'#%02X%02X%02X' % (r(),r(),r())
        fill = "#ffffff"
        img1.rectangle([room.fromPosition.toTuple(),room.toPosition.toTuple()], fill=fill)

    for idx,wall in enumerate(wallsobj):
        fill = "#eee"
        if wall.isOuterWall:
            fill = "#000"
        
        # r = lambda: random.randint(0,255)
        # fill = f'#%02X%02X%02X' % (r(),r(),r())
        img1.rectangle([(wall.fromPosition.x,wall.fromPosition.y),(wall.toPosition.x,wall.toPosition.y)], fill)

        for feature in wall.features:
            if feature.type == FeatureType.DOOR:
                fr = [wall.fromPosition.x,wall.fromPosition.y]
                to = [wall.fromPosition.x,wall.fromPosition.y]

                frHinge = [wall.fromPosition.x,wall.fromPosition.y]
                toHinge = [wall.fromPosition.x,wall.fromPosition.y]

                frOpen = [wall.fromPosition.x,wall.fromPosition.y]
                toOpen = [wall.fromPosition.x,wall.fromPosition.y]

                if wall.isHorizontal:

                    frHinge[0] = frHinge[0] + feature.hinge + (wall_width if feature.hinge==feature.fromPosition else 0)
                    toHinge[0] = toHinge[0] + feature.hinge + (-wall_width if feature.hinge!=feature.fromPosition else 0)
                    toHinge[1] = toHinge[1] + wall_width

                    fr[0] = fr[0] + feature.fromPosition
                    to[0] = to[0] + feature.toPosition
                    to[1] = to[1] + wall_width

                    frOpen[0] = frOpen[0] + feature.hinge + (wall_width if feature.hinge==feature.fromPosition else 0)
                    frOpen[1] = frOpen[1] + (-wall_width if feature.openLeft else wall_width)
                    toOpen[0] = toOpen[0] + feature.hinge + (-wall_width if feature.hinge!=feature.fromPosition else 0)
                    toOpen[1] = toOpen[1] + wall_width + (-wall_width if feature.openLeft else wall_width)

                else:
                    frHinge[0] = frHinge[0] - wall_width
                    frHinge[1] = frHinge[1] + feature.hinge + (wall_width if feature.hinge==feature.fromPosition else 0)
                    toHinge[1] = toHinge[1] + feature.hinge + (-wall_width if feature.hinge!=feature.fromPosition else 0)

                    fr[0] = fr[0] - wall_width
                    fr[1] = fr[1] + feature.fromPosition
                    to[1] = to[1] + feature.toPosition

                    frOpen[0] = frOpen[0] + (-wall_width if feature.openLeft else wall_width) - wall_width
                    frOpen[1] = frOpen[1] + feature.hinge + (wall_width if feature.hinge==feature.fromPosition else 0)
                    toOpen[0] = toOpen[0] + (-wall_width if feature.openLeft else wall_width)
                    toOpen[1] = toOpen[1] + feature.hinge + (-wall_width if feature.hinge!=feature.fromPosition else 0)

                img1.rectangle([tuple(fr),tuple(to)], fill="#f00")
                img1.rectangle([tuple(frHinge),tuple(toHinge)], fill="#000")
                img1.rectangle([tuple(frOpen),tuple(toOpen)], fill="#f00")
            elif feature.type==FeatureType.WINDOW:
                fr = [wall.fromPosition.x,wall.fromPosition.y]
                to = [wall.fromPosition.x,wall.fromPosition.y]
                if wall.isHorizontal:

                    fr[0] = fr[0] + feature.fromPosition
                    to[0] = to[0] + feature.toPosition
                    to[1] = to[1] + wall_width

                else:
                    fr[0] = fr[0] - wall_width
                    fr[1] = fr[1] + feature.fromPosition
                    to[1] = to[1] + feature.toPosition

                r = lambda: random.randint(0,255)
                fill = f'#%02X%02X%02X' % (r(),r(),r())
                fill = "#00f"
                img1.rectangle([tuple(fr),tuple(to)], fill=fill)



    for idx,junc in enumerate(junctions):
        outline = "#f00"
        if junctions[idx]["outerwall"]:
            outline = "#f00"
        pos = [
            [junc["left"]-wall_width_half, junc["top"]-wall_width_half],
            [junc["left"]+wall_width_half, junc["top"]+wall_width_half],
        ]
        if junc["corner"]["left"]!=None:
            pos[0][0] = pos[0][0] - 20
        if junc["corner"]["right"]!=None:
            pos[1][0] = pos[1][0] + 20
        if junc["corner"]["top"]!=None:
            pos[0][1] = pos[0][1] - 20
        if junc["corner"]["bottom"]!=None:
            pos[1][1] = pos[1][1] + 20

    # if CONFIG.getSAVE_TEMP():
    #     im.save("whh copy 2.jpg")

    # print(sys.argv)

    # r = int(sys.argv[1])
    # img1.rectangle([rooms[r].fromPosition.toTuple(),rooms[r].toPosition.toTuple()], fill="#f00")

    if CONFIG.getSAVE_STATIC():
        filename = f"images/{time.time()}.jpg"
        im.save(filename)
    if CONFIG.getSAVE_TEMP():
        im.save("whh.jpg")

def drawAndReturnFromDatabase(junctions,wallsobj:List,rooms:List):
    xmin = 99999999999
    xmax = 0
    ymin = 99999999999
    ymax = 0

    for wall in wallsobj:
        if xmin > wall["fromPosition"]["x"]:
            xmin = wall["fromPosition"]["x"]
        if xmax < wall["toPosition"]["x"]:
            xmax = wall["toPosition"]["x"]
        if ymin > wall["fromPosition"]["y"]:
            ymin = wall["fromPosition"]["y"]
        if ymax < wall["toPosition"]["y"]:
            ymax = wall["toPosition"]["y"]

    w = xmax - xmin + 200
    h = ymax - ymin + 200
    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
    img1 = ImageDraw.Draw(im)

    wall_width = 10
    wall_width_half = wall_width/2

    def toTuple(inp):
        return (inp["x"],inp["y"])

    for room in rooms:
        r = lambda: random.randint(0,255)
        fill = f'#%02X%02X%02X' % (r(),r(),r())
        fill = "#ffffff"
        img1.rectangle([toTuple(room["fromPosition"]),toTuple(room["toPosition"])], fill=fill)

    for idx,wall in enumerate(wallsobj):
        fill = "#eee"
        if wall["isOuterWall"]:
            fill = "#000"
        
        # r = lambda: random.randint(0,255)
        # fill = f'#%02X%02X%02X' % (r(),r(),r())
        img1.rectangle([(wall["fromPosition"]["x"],wall["fromPosition"]["y"]),(wall["toPosition"]["x"],wall["toPosition"]["y"])], fill)

        for feature in wall["features"]:
            if feature["type"] == "DOOR":
                fr = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]
                to = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]

                frHinge = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]
                toHinge = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]

                frOpen = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]
                toOpen = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]

                if wall["isHorizontal"]:

                    frHinge[0] = frHinge[0] + feature["hinge"] + (wall_width if feature["hinge"]==feature["fromPosition"] else 0)
                    toHinge[0] = toHinge[0] + feature["hinge"] + (-wall_width if feature["hinge"]!=feature["fromPosition"] else 0)
                    toHinge[1] = toHinge[1] + wall_width

                    fr[0] = fr[0] + feature["fromPosition"]
                    to[0] = to[0] + feature["toPosition"]
                    to[1] = to[1] + wall_width

                    frOpen[0] = frOpen[0] + feature["hinge"] + (wall_width if feature["hinge"]==feature["fromPosition"] else 0)
                    frOpen[1] = frOpen[1] + (-wall_width if feature["openLeft"] else wall_width)
                    toOpen[0] = toOpen[0] + feature["hinge"] + (-wall_width if feature["hinge"]!=feature["fromPosition"] else 0)
                    toOpen[1] = toOpen[1] + wall_width + (-wall_width if feature["openLeft"] else wall_width)

                else:
                    frHinge[0] = frHinge[0] - wall_width
                    frHinge[1] = frHinge[1] + feature["hinge"] + (wall_width if feature["hinge"]==feature["fromPosition"] else 0)
                    toHinge[1] = toHinge[1] + feature["hinge"] + (-wall_width if feature["hinge"]!=feature["fromPosition"] else 0)

                    fr[0] = fr[0] - wall_width
                    fr[1] = fr[1] + feature["fromPosition"]
                    to[1] = to[1] + feature["toPosition"]

                    frOpen[0] = frOpen[0] + (-wall_width if feature["openLeft"] else wall_width) - wall_width
                    frOpen[1] = frOpen[1] + feature["hinge"] + (wall_width if feature["hinge"]==feature["fromPosition"] else 0)
                    toOpen[0] = toOpen[0] + (-wall_width if feature["openLeft"] else wall_width)
                    toOpen[1] = toOpen[1] + feature["hinge"] + (-wall_width if feature["hinge"]!=feature["fromPosition"] else 0)

                img1.rectangle([tuple(fr),tuple(to)], fill="#f00")
                img1.rectangle([tuple(frHinge),tuple(toHinge)], fill="#000")
                img1.rectangle([tuple(frOpen),tuple(toOpen)], fill="#f00")
            elif feature["type"]=="WINDOW":
                fr = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]
                to = [wall["fromPosition"]["x"],wall["fromPosition"]["y"]]
                if wall["isHorizontal"]:

                    fr[0] = fr[0] + feature["fromPosition"]
                    to[0] = to[0] + feature["toPosition"]
                    to[1] = to[1] + wall_width

                else:
                    fr[0] = fr[0] - wall_width
                    fr[1] = fr[1] + feature["fromPosition"]
                    to[1] = to[1] + feature["toPosition"]

                r = lambda: random.randint(0,255)
                fill = f'#%02X%02X%02X' % (r(),r(),r())
                fill = "#00f"
                img1.rectangle([tuple(fr),tuple(to)], fill=fill)



    for idx,junc in enumerate(junctions):
        outline = "#f00"
        if junctions[idx]["outerwall"]:
            outline = "#f00"
        pos = [
            [junc["left"]-wall_width_half, junc["top"]-wall_width_half],
            [junc["left"]+wall_width_half, junc["top"]+wall_width_half],
        ]
        if junc["corner"]["left"]!=None:
            pos[0][0] = pos[0][0] - 20
        if junc["corner"]["right"]!=None:
            pos[1][0] = pos[1][0] + 20
        if junc["corner"]["top"]!=None:
            pos[0][1] = pos[0][1] - 20
        if junc["corner"]["bottom"]!=None:
            pos[1][1] = pos[1][1] + 20

    

    # if CONFIG.getSAVE_TEMP():
    #     im.save("whh copy 2.jpg")

    # print(sys.argv)

    # r = int(sys.argv[1])
    # img1.rectangle([rooms[r].fromPosition.toTuple(),rooms[r].toPosition.toTuple()], fill="#f00")

    # if CONFIG.getSAVE_STATIC():
    #     filename = f"images/{time.time()}.jpg"
    #     im.save(filename)
    # if CONFIG.getSAVE_TEMP():
    #     im.save("whh.jpg")
    return im
