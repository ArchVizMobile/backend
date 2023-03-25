import numpy as np
from PIL import Image, ImageDraw
import time
from config import CONFIG

def draw(walls):
    w = CONFIG.getIMAGE_WIDTH()
    h = CONFIG.getIMAGE_HEIGHT()
    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
    img1 = ImageDraw.Draw(im)

    wall_width = 0
    wall_width_half = wall_width/2


    rooms = [
        [[100,100,True,"#000000"]],
    ]

    for idx,wall in enumerate(walls):
        fill = "#000"
        img1.rectangle([(wall[0][0][0],wall[0][0][1]),(wall[0][1][0],wall[0][1][1])], fill)
        # if wall[1] and random.random() > 0.9 and wall[0][1][0]-wall[0][0][0] > 140:
        #     w = wall[0]
        #     w[0][0] = int(random.randrange(w[0][0] + 20,int(w[0][0] + 20 +(random.random()*20))))
        #     w[1][0] = w[0][0] + 100
        #     img1.rectangle([(w[0][0],w[0][1]),(w[1][0],w[1][1])], fill = "#fff")
        # if not wall[1] and random.random() > 0.9 and wall[0][0][1]-wall[0][0][0] > 140:
        #     w = wall[0]
        #     w[0][1] = int(random.randrange(w[0][1] + 20,int(w[0][1] + 20 +(random.random()*20))))
        #     w[1][1] = w[0][1] + 100
        #     img1.rectangle([(w[0][0],w[0][1]),(w[1][0],w[1][1])], fill = "#fff")

    for room in rooms:
        for r in room:
            img1.rectangle([
                (r[0]-wall_width_half, r[1]-wall_width_half),
                (r[0]+wall_width_half, r[1]+wall_width_half),
            ], fill = "#000")
    if CONFIG.getSAVE_STATIC():
        filename = f"images/{time.time()}.jpg"
        im.save(filename)
    if CONFIG.getSAVE_TEMP():
        im.save("whh.jpg")

