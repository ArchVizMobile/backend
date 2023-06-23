from PIL import Image, ImageChops, ImageDraw
import jsonpickle
import numpy
import sys
import logging

logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

# logging.debug("debug test")
# logging.warning("debug test")
# logging.error("debug test")

cut_top = 150 #350
cut_bottom = 50
cut_left = 50 #400
cut_right = 50
grid_size = 38

color_wall = (0,0,0)
color_window = (4,77,132)
color_door = (230,25,42)
grid_color = (202,235,253)

def pilToNumpy(img):
    return numpy.array(img)

def NumpyToPil(img):
    return Image.fromarray(img)

def trim(im, color):
    bg = Image.new(im.mode, im.size, color)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def colors_match(el,target,offset=10):
    return el+offset > target and el-offset < target

def color_in_array(color,arr):
    for y in arr:
        for el in y:
            if colors_do_match(el,color):
                return True
    return False

def colors_do_match(el,target,offset=10):
    return  colors_match(el[0],target[0],offset) and \
            colors_match(el[1],target[1],offset) and \
            colors_match(el[2],target[2],offset)

def parseImage(im):
    logging.debug("[parseImage] Init")
    pix = pilToNumpy(im)
    pix = pix[cut_top:-cut_bottom, cut_left:-cut_right]
    
    prev_grid = {
        "x": {},
        "y": {}
    }

    topmost_y = 9999
    topmost_x = 9999
    smollmost_y = -1
    smollmost_x = -1

    logging.debug("[parseImage] Getting Grid")
    progress = 0
    for y in range(0,len(pix)):
        p = round(y*100/len(pix))
        if p!=progress:
            progress = p
            logging.debug(f"[parseImage::GRID] {progress}%")
        for x in range(0,len(pix[y])):
            try:
                insideY = y > 0 and y < len(pix)-1
                insideX = x > 0 and x < len(pix[y])-1
                isInside = insideX and insideY

                if isInside and \
                    colors_do_match(pix[y][x],grid_color,1) and \
                    ((x > 0 and colors_do_match(pix[y][x-1],grid_color,1)) or x==0) and \
                    ((x < len(pix[y]) and colors_do_match(pix[y][x+1],grid_color,1)) or x==len(pix[y])) and \
                    ((y < len(pix) and colors_do_match(pix[y+1][x],grid_color,1)) or y==len(pix)) and \
                    ((y > 0 and colors_do_match(pix[y-1][x],grid_color,1)) or y==0):
                    if y not in prev_grid["y"]:
                        prev_grid["y"][y] = True
                    if x not in prev_grid["x"]:
                        prev_grid["x"][x] = True
                    pix[y][x] = (255,255,255)
                    if smollmost_x < x:
                        smollmost_x = x
                    if smollmost_y < y:
                        smollmost_y = y
                elif not colors_do_match(pix[y][x],(255,255,255),2):
                    if topmost_y==9999:
                        topmost_y=y
                    if topmost_x > x:
                        topmost_x = x
            except:
                logging.debug(f"error {x}:{y}")
                pass
    
    logging.debug("[parseImage] Got Grid - Cutting Image")

    # logging.debug(prev_grid)
    sorted_x = sorted(list(prev_grid["x"].keys()))
    sorted_y = sorted(list(prev_grid["y"].keys()))
    # logging.debug(sorted_x)

    def findClosest(el,arr):
        last_el = arr[0]
        for item in arr:
            # logging.debug(item)
            if item > el:
                return last_el
            last_el = item

    closest_x = -1
    closest_y = -1
    for y in range(0,len(pix)):
        for x in range(0,len(pix[y])):
            if y==topmost_y:
                if closest_y==-1:
                    closest_y = findClosest(y,sorted_y)
                    # logging.debug("closest_y",closest_y)
                # pix[closest_y][x] = (255,0,0)
            if x==topmost_x:
                if closest_x==-1:
                    closest_x = findClosest(x,sorted_x)
                    # logging.debug("closest_x",closest_x)
                # pix[y][closest_x] = (255,0,0)

    # print(closest_y,smollmost_y, closest_x,smollmost_x)
    # sys.exit()

    pix = pix[closest_y:smollmost_y, closest_x:smollmost_x]
    
    logging.debug("[parseImage] Image Cut - Building Matrix")

    gridmatrix = {
        "x":[],
        "y":[]
    }

    for y in range(0,len(pix)):
        if colors_do_match(pix[y][closest_x-1],grid_color,2):
            gridmatrix["y"].append(y)
            
    for x in range(0,len(pix[0])):
        if colors_do_match(pix[closest_y-1][x],grid_color,2):
            gridmatrix["x"].append(x)
    
    for idx,x in enumerate(gridmatrix["x"]):
        if idx < len(gridmatrix["x"])-1:
            gridmatrix["x"][idx] = {"from":gridmatrix["x"][idx]+1,"to":gridmatrix["x"][idx+1]-1}
        else:
            del gridmatrix["x"][idx]

    for idx,y in enumerate(gridmatrix["y"]):
        if idx < len(gridmatrix["y"])-1:
            gridmatrix["y"][idx] = {"from":gridmatrix["y"][idx]+1,"to":gridmatrix["y"][idx+1]-1}
        else:
            del gridmatrix["y"][idx]

    gridmatrix2 = []

    for xidx,x in enumerate(gridmatrix["x"]):
        for yidx,y in enumerate(gridmatrix["y"]):
            if xidx < len(gridmatrix["x"])-1 and yidx < len(gridmatrix["y"])-1:
                gridmatrix2.append({
                    "from": {
                        "x": x["from"],
                        "y": y["from"]
                    },
                    "to": {
                        "x": x["to"],
                        "y": y["to"],
                    }
                })
    # logging.debug(gridmatrix2)
    logging.debug("[parseImage] Matrix Built - Converting")
                
    img = NumpyToPil(pix).convert('RGB')
    # img = trim(NumpyToPil(pix).convert('RGB'),(255,255,255))
    pix = pilToNumpy(img)
    image = Image.new('RGB', (len(pix[0]), len(pix)), (255, 255, 255))
    image1 = Image.new('RGB', (len(pix[0]), len(pix)), (255, 255, 255))

    img = NumpyToPil(pix)

    draw = ImageDraw.Draw(img)
    draw1 = ImageDraw.Draw(image)
    draw2 = ImageDraw.Draw(image1)

    logging.debug("[parseImage] Converted - Drawing Grid")
    
    # for item in gridmatrix2:
        # draw.line((item["from"]["x"]-1,item["from"]["y"]-1,item["from"]["x"]-1,item["to"]["y"]+1),fill="red")
        # draw.line((item["from"]["x"]-1,item["from"]["y"]-1,item["to"]["x"]+1,item["from"]["y"]-1),fill="red")

    # img.save("grid.png")
    logging.debug("[parseImage] Grid drawn to grid.png - Building Junctions & Features")
    # sys.exit()
    junctions = []

    # for y in range(0,len(pix),grid_size):
    #     for x in range(0,len(pix[y]),grid_size):
    progress = 0
    for idx,item in enumerate(gridmatrix2):
        p = round(idx*100/len(gridmatrix2))
        if progress!=p:
            progress = p
            logging.debug(f"[parseImage::JUNCTIONS] {progress}%")

        # if x>0 and y>0:
        # {
        #     "from": {
        #         "x": x+1,
        #         "y": y+1
        #     },
        #     "to": {
        #         "x": gridmatrix["x"][xidx+1]-1,
        #         "y": gridmatrix["y"][yidx+1]-1,
        #     }
        # }
        pos_from_y = item["from"]["y"]
        pos_to_y = item["to"]["y"]
        pos_from_x = item["from"]["x"]
        pos_to_x = item["to"]["x"]
        group = pix[pos_from_y:pos_to_y,pos_from_x:pos_to_x]
        wall_bottom = False
        wall_top = False
        wall_left = False
        wall_right = False
        window = False
        door = False

        window = color_in_array(color_window,group)
        door = color_in_array(color_door,group)

        wall_bottom = color_in_array(color_wall,group[-3:-1,0:-1])
        wall_top = color_in_array(color_wall,group[0:3,0:-1])
        wall_left = color_in_array(color_wall,group[0:-1,0:3])
        wall_right = color_in_array(color_wall,group[0:-1,-3:-1])
        wall = wall_bottom or wall_top or wall_left or wall_right

        # logging.debug(window,wall_bottom,wall_top,wall_left,wall_right)
        
        if wall_bottom:
            draw.line((pos_from_x,pos_to_y,pos_to_x,pos_to_y), fill=color_wall)
        if wall_top:
            draw.line((pos_from_x,pos_from_y,pos_to_x,pos_from_y), fill=color_wall)
        if wall_left:
            draw.line((pos_from_x,pos_from_y,pos_from_x,pos_to_y), fill=color_wall)
        if wall_right:
            draw.line((pos_to_x,pos_from_y,pos_to_x,pos_to_y), fill=color_wall)

        if window and wall:
            draw.rectangle((pos_from_x,pos_from_y,pos_to_x,pos_to_y),outline=(0,0,255))

        if door and wall:
            draw.rectangle((pos_from_x,pos_from_y,pos_to_x,pos_to_y),outline=(255,0,0))

        # if wall_right:
            # draw1.line((x-(grid_size/2),y-(grid_size/2),x,y-(grid_size/2)), fill=color_wall,width=5)
        
        # if wall_left:
            # draw1.line((x-(grid_size),y-(grid_size/2),x-(grid_size/2),y-(grid_size/2)), fill=color_wall,width=5)
        
        # if wall_top:
            # draw1.line((x-(grid_size/2),y-(grid_size),x-(grid_size/2),y-(grid_size/2)), fill=color_wall,width=5)
        
        # if wall_bottom:
            # draw1.line((x-(grid_size/2),y-(grid_size/2),x-(grid_size/2),y), fill=color_wall,width=5)
        
        horizontal = wall_left and wall_right and not wall_top and not wall_bottom
        vertical = not wall_left and not wall_right and wall_top and wall_bottom

        feature_offset = 5

        # if door:
            # if horizontal:
                # draw1.line((x-(grid_size/2),y-(grid_size/2)-feature_offset,x-(grid_size/2),y-(grid_size/2)+feature_offset),fill=color_door,width=5)
            # if vertical:
                # draw1.line((x-(grid_size/2)-feature_offset,y-(grid_size/2),x-(grid_size/2)+feature_offset,y-(grid_size/2)),fill=color_door,width=5)

        # if window:
            # if horizontal:
                # draw1.line((x-(grid_size/2),y-(grid_size/2)-feature_offset,x-(grid_size/2),y-(grid_size/2)+feature_offset),fill=color_window,width=5)
            # if vertical:
                # draw1.line((x-(grid_size/2)-feature_offset,y-(grid_size/2),x-(grid_size/2)+feature_offset,y-(grid_size/2)),fill=color_window,width=5)

        # pos_x = x-(grid_size/2)
        # pos_y = y-(grid_size/2)

        
        junction = {
            "x":x,
            "y":y,
            "left":wall_left,
            "right":wall_right,
            "bottom":wall_bottom,
            "top":wall_top,
            "window":window,
            "door":door,
        }
        junctions.append(junction)
        gridmatrix2[idx]["junction"] = junction
        # mastergrid[f"{int(x-(grid_size/2))}:{int(y-(grid_size/2))}"] = junction

        # if wall_right and wall_bottom and not wall_left and not wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,0,0))
            
        # if wall_right and not wall_bottom and not wall_left and wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,123,0))
            
        # if not wall_right and not wall_bottom and wall_left and wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,0,123))
            
        # if not wall_right and wall_bottom and wall_left and not wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(0,255,123))
            
        # if wall_right and wall_bottom and wall_left and not wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(0,123,123))
            
        # if wall_right and not wall_bottom and wall_left and wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(123,255,123))
            
        # if wall_right and wall_bottom and not wall_left and wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,255,123))
            
        # if not wall_right and wall_bottom and  wall_left and wall_top:
            # draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,123,255))
    # logging.debug(jsonpickle.encode(gridmatrix2,unpicklable=False))
    #  {
    #   'from': {'x': 152, 'y': 492},
    #   'to': {'x': 188, 'y': 528}, 
    #   'junction': { 'x': {'from': 871, 'to': 906}, 
    #       'y': {'from': 757, 'to': 793}, 'left': False, 'right': False, 'bottom': False, 'top': False, 'window': False, 'door': False}},
    junctionz = []
    for item in gridmatrix2:
        n = 0
        if "junction" in item:
            vertical = item["junction"]["left"] and item["junction"]["right"]
            horizontal = item["junction"]["top"] and item["junction"]["left"]
            if item["junction"]["left"]:
                n = n + 1
            if item["junction"]["right"]:
                n = n + 1
            if item["junction"]["bottom"]:
                n = n + 1
            if item["junction"]["top"]:
                n = n + 1
        if (n == 2 and not vertical and not horizontal) or n > 2:
            junctionz.append({
                "x":item["from"]["x"] + ((item["to"]["x"]-item["from"]["x"])/2),
                "y":item["from"]["y"] + ((item["to"]["y"]-item["from"]["y"])/2),
                "generated":False,
            })
    logging.debug(gridmatrix2)
    logging.debug(junctionz)
    img.save("temp.png")
    image.save("temp1.png")
    image1.save("temp2.png")
    # sys.exit()
    return junctionz
    
    # logging.debug(jsonpickle.encode(mastergrid,unpicklable=False))
    # logging.debug(mastergrid)

    for key in mastergrid:
        item = mastergrid[key]
        if item!=None:
            x = item["x"]-(grid_size/2)
            y = item["y"]-(grid_size/2)

            # print(x,y,key)

            # if t=="315:245":
            #     print(jsonpickle.encode({
            #         "t":t,
            #         "in_mastergrid":t in mastergrid,
            #         "key":key,
            #         "item":mastergrid[key],
            #         "opposite": mastergrid[t]
            #     },unpicklable=False,indent=2))
            if item["window"] or item["door"]:

                if item["left"] or item["right"]:
                    item["left"] = True
                    item["right"] = True

                if item["bottom"] or item["top"]:
                    item["bottom"] = True
                    item["top"] = True

            def checkDirection(t,dir):
                return (
                    (t in mastergrid and mastergrid[t]!=None and mastergrid[t][dir]==False) or 
                    (t not in mastergrid) or
                    (t in mastergrid and mastergrid[t]==None)
                )
            t = f"{int(x-grid_size)}:{int(y)}"
            if item["left"] and checkDirection(t,"right"):
                mastergrid[key]["left"] = None
                print("item gone")

            t = f"{int(x+grid_size)}:{int(y)}"
            if item["right"] and checkDirection(t,"left"):
                mastergrid[key]["right"] = None
                print("item gone")

            t = f"{int(x)}:{int(y-grid_size)}"
            if item["top"] and checkDirection(t,"bottom"):
                mastergrid[key]["top"] = None
                print("item gone")
            
            t = f"{int(x)}:{int(y+grid_size)}"
            if item["bottom"] and checkDirection(t,"top"):
                mastergrid[key]["bottom"] = None
                print("item gone")
        
        # print(key)

    # for j in junctions:
        # for i in junctions:
            # if j["top"] and i["bottom"]

    for key in mastergrid:
        junction = mastergrid[key]
        if junction!=None:
            x = junction["x"]
            y = junction["y"]
            door = junction["door"]
            window = junction["window"]
            if junction["right"]:
                draw2.line((x,y,x+(grid_size/2),y), fill=color_wall,width=5)
            
            if junction["left"]:
                draw2.line((x-(grid_size/2),y,x,y), fill=color_wall,width=5)
            
            if junction["top"]:
                draw2.line((x,y-(grid_size/2),x,y), fill=color_wall,width=5)
            
            if junction["bottom"]:
                draw2.line((x,y,x,y+(grid_size/2)), fill=color_wall,width=5)
            
            horizontal = junction["left"] and junction["right"] and not junction["top"] and not junction["bottom"]
            vertical = not junction["left"] and not junction["right"] and junction["top"] and junction["bottom"]

            feature_offset = 5

            if door:
                if horizontal:
                    draw2.line((x,y-feature_offset,x,y+feature_offset),fill=color_door,width=5)
                if vertical:
                    draw2.line((x-feature_offset,y,x+feature_offset,y),fill=color_door,width=5)

            if window:
                if horizontal:
                    draw2.line((x,y-feature_offset,x,y+feature_offset),fill=color_window,width=5)
                if vertical:
                    draw2.line((x-feature_offset,y,x+feature_offset,y),fill=color_window,width=5)

            # draw2.line((x-5,y-5,x+5,y+5),fill=color_door,width=2)
            # draw2.line((x+5,y-5,x-5,y+5),fill=color_door,width=2)
            # draw2.text((x,y),f"{int(x-(grid_size/2))}:{int(y-(grid_size/2))}",fill=color_door)

    img.save("temp.png")
    image.save("temp1.png")
    image1.save("temp2.png")
    # img.show()


# while True:
# screenshot = ImageGrab.grab()  # Take the screenshot
# screenshot = screenshot.crop((0,0,screenshot.width,screenshot.height))
# screenshot.save("screenshot.png")
# parseImage(screenshot)
with Image.open("screenshot.png") as im:
    parseImage(im)
