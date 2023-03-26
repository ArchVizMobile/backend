import json
from typing import List
import jsonpickle
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import time
from APIResponse import Wall
from config import CONFIG

def draw(walls,junctions,wallsobj:List[Wall]):
    w = CONFIG.getIMAGE_WIDTH()
    h = CONFIG.getIMAGE_HEIGHT()
    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
    img1 = ImageDraw.Draw(im)

    wall_width = CONFIG.getWALL_WIDTH()
    wall_width_half = wall_width/2

    for idx,wall in enumerate(wallsobj):
        fill = "#000"
        if wall.isOuterWall:
            fill = "#999"
        img1.rectangle([(wall.fromPosition.x,wall.fromPosition.y),(wall.toPosition.x,wall.toPosition.y)], fill)
        if wall.isHorizontal:
            # print(wall)
            fr = [wall.fromPosition.x,wall.fromPosition.y]
            to = [wall.fromPosition.x,wall.fromPosition.y]

            frHinge = [wall.fromPosition.x,wall.fromPosition.y]
            toHinge = [wall.fromPosition.x,wall.fromPosition.y]

            for door in wall.doors:
                if wall.isHorizontal:
                    
                    frHinge[0] = frHinge[0] + door.hinge
                    toHinge[0] = toHinge[0] + door.hinge+wall_width
                    toHinge[1] = toHinge[1] + wall_width

                    fr[0] = fr[0] + door.fromPosition
                    to[0] = to[0] + door.toPosition
                    to[1] = to[1] + wall_width
                else:
                    frHinge[1] = frHinge[1] + door.hinge
                    toHinge[1] = toHinge[1] + door.hinge+wall_width
                    toHinge[0] = toHinge[0] + wall_width

                    fr[1] = fr[1] + door.fromPosition
                    to[1] = to[1] + door.toPosition
                    to[0] = to[0] + wall_width
                img1.rectangle([tuple(fr),tuple(to)], fill="#f00")
                img1.rectangle([tuple(frHinge),tuple(toHinge)], fill="#000")

    # print(json.dumps(junctions))

    for idx,junc in enumerate(junctions):
        # junctions[idx]["outerwall"] = False
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
    
    if CONFIG.getSAVE_STATIC():
        filename = f"images/{time.time()}.jpg"
        im.save(filename)
    if CONFIG.getSAVE_TEMP():
        im.save("whh.jpg")

