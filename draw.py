import json
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import time
from config import CONFIG

def draw(walls,junctions,wallsobj):
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
        if wall["isOuterWall"]:
            fill = "#999"
        img1.rectangle([(wall["from"]["x"],wall["from"]["y"]),(wall["to"]["x"],wall["to"]["y"])], fill)
        if wall["isHorizontal"]:
            # print(wall)
            for door in wall["doors"]:
                # img1.rectangle([
                #     # +(door["width"] if door["hinge"][0] else 0)
                #     (door["from"]["x"],door["from"]["y"]),
                #     (door["to"]["x"],door["to"]["y"])
                # ], fill="#f00")
                # if door["hinge"][0]:
                # img1.rectangle([
                #     # +(door["width"] if door["hinge"][0] else 0)
                #     (
                #         door["from"]["x"]+(0 if door["hinge"][0] else door["width"]),
                #         door["from"]["y"]+(10 if door["hinge"][2] else door["width"])-10
                #     ),
                #     (
                #         door["from"]["x"]+10+(0 if door["hinge"][0] else door["width"]),
                #         door["from"]["y"]+10+(10 if door["hinge"][2] else door["width"])-10
                #     )
                # ], fill="#000")
                print(door)

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

