from PIL import Image, ImageChops, ImageDraw
import numpy
import sys

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
    pix = pilToNumpy(im)
    pix = pix[cut_top:-cut_bottom, cut_left:-cut_right]

    for y in range(0,len(pix)):
        for x in range(0,len(pix[y])):
            if colors_do_match(pix[y][x],grid_color,2):
                pix[y][x] = (255,255,255)
    img = NumpyToPil(pix).convert('RGB')
    # img = trim(NumpyToPil(pix).convert('RGB'),(255,255,255))
    img.save("before.png")
    sys.exit()
    print("before")
    pix = pilToNumpy(img)
    image = Image.new('RGB', (len(pix[0]), len(pix)), (255, 255, 255))
    image1 = Image.new('RGB', (len(pix[0]), len(pix)), (255, 255, 255))

    img = NumpyToPil(pix)

    draw = ImageDraw.Draw(img)
    draw1 = ImageDraw.Draw(image)
    draw2 = ImageDraw.Draw(image1)

    mastergrid = {}
    for y in range(0,len(pix),grid_size):
        for x in range(0,len(pix[y]),grid_size):
            mastergrid[f"{int(x-(grid_size/2))}:{int(y-(grid_size/2))}"] = None

    junctions = []

    for y in range(0,len(pix),grid_size):
        for x in range(0,len(pix[y]),grid_size):
            if x>0 and y>0:

                group = pix[y-grid_size:y,x-grid_size:x]
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

                # print(window,wall_bottom,wall_top,wall_left,wall_right)
                
                if wall_bottom:
                    draw.line((x-grid_size,y,x,y), fill=color_wall)
                if wall_top:
                    draw.line((x-grid_size,y-grid_size,x,y-grid_size), fill=color_wall)
                if wall_left:
                    draw.line((x-grid_size,y-grid_size,x-grid_size,y), fill=color_wall)
                if wall_right:
                    draw.line((x,y-grid_size,x,y), fill=color_wall)

                if window and wall:
                    draw.rectangle((x-grid_size,y-grid_size,x,y),outline=(0,0,255))

                if door and wall:
                    draw.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,0,0))

                if wall_right:
                    draw1.line((x-(grid_size/2),y-(grid_size/2),x,y-(grid_size/2)), fill=color_wall,width=5)
                
                if wall_left:
                    draw1.line((x-(grid_size),y-(grid_size/2),x-(grid_size/2),y-(grid_size/2)), fill=color_wall,width=5)
                
                if wall_top:
                    draw1.line((x-(grid_size/2),y-(grid_size),x-(grid_size/2),y-(grid_size/2)), fill=color_wall,width=5)
                
                if wall_bottom:
                    draw1.line((x-(grid_size/2),y-(grid_size/2),x-(grid_size/2),y), fill=color_wall,width=5)
                
                horizontal = wall_left and wall_right and not wall_top and not wall_bottom
                vertical = not wall_left and not wall_right and wall_top and wall_bottom

                feature_offset = 5

                if door:
                    if horizontal:
                        draw1.line((x-(grid_size/2),y-(grid_size/2)-feature_offset,x-(grid_size/2),y-(grid_size/2)+feature_offset),fill=color_door,width=5)
                    if vertical:
                        draw1.line((x-(grid_size/2)-feature_offset,y-(grid_size/2),x-(grid_size/2)+feature_offset,y-(grid_size/2)),fill=color_door,width=5)

                if window:
                    if horizontal:
                        draw1.line((x-(grid_size/2),y-(grid_size/2)-feature_offset,x-(grid_size/2),y-(grid_size/2)+feature_offset),fill=color_window,width=5)
                    if vertical:
                        draw1.line((x-(grid_size/2)-feature_offset,y-(grid_size/2),x-(grid_size/2)+feature_offset,y-(grid_size/2)),fill=color_window,width=5)

                pos_x = x-(grid_size/2)
                pos_y = y-(grid_size/2)

                
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
                mastergrid[f"{int(x-(grid_size/2))}:{int(y-(grid_size/2))}"] = junction

                if wall_right and wall_bottom and not wall_left and not wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,0,0))
                    
                if wall_right and not wall_bottom and not wall_left and wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,123,0))
                    
                if not wall_right and not wall_bottom and wall_left and wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,0,123))
                    
                if not wall_right and wall_bottom and wall_left and not wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(0,255,123))
                    
                if wall_right and wall_bottom and wall_left and not wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(0,123,123))
                    
                if wall_right and not wall_bottom and wall_left and wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(123,255,123))
                    
                if wall_right and wall_bottom and not wall_left and wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,255,123))
                    
                if not wall_right and wall_bottom and  wall_left and wall_top:
                    draw1.rectangle((x-grid_size,y-grid_size,x,y),outline=(255,123,255))
    # mastergrid = jsonpickle.decode('{"-35:-35": null, "35:-35": null, "105:-35": null, "175:-35": null, "245:-35": null, "315:-35": null, "385:-35": null, "455:-35": null, "525:-35": null, "595:-35": null, "665:-35": null, "735:-35": null, "805:-35": null, "875:-35": null, "945:-35": null, "1015:-35": null, "1085:-35": null, "1155:-35": null, "1225:-35": null, "-35:35": null, "35:35": {"x": 70, "y": 70, "left": false, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "105:35": {"x": 140, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "175:35": {"x": 210, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "245:35": {"x": 280, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "315:35": {"x": 350, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "385:35": {"x": 420, "y": 70, "left": true, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "455:35": {"x": 490, "y": 70, "left": true, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "525:35": {"x": 560, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "595:35": {"x": 630, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "665:35": {"x": 700, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "735:35": {"x": 770, "y": 70, "left": true, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "805:35": {"x": 840, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "875:35": {"x": 910, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "945:35": {"x": 980, "y": 70, "left": true, "right": true, "bottom": true, "top": false, "window": true, "door": false}, "1015:35": {"x": 1050, "y": 70, "left": true, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "1085:35": {"x": 1120, "y": 70, "left": true, "right": true, "bottom": true, "top": false, "window": true, "door": false}, "1155:35": {"x": 1190, "y": 70, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "1225:35": {"x": 1260, "y": 70, "left": true, "right": false, "bottom": true, "top": false, "window": false, "door": false}, "-35:105": null, "35:105": {"x": 70, "y": 140, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "105:105": {"x": 140, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:105": {"x": 210, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:105": {"x": 280, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:105": {"x": 350, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:105": {"x": 420, "y": 140, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "455:105": {"x": 490, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "525:105": {"x": 560, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "595:105": {"x": 630, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "665:105": {"x": 700, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:105": {"x": 770, "y": 140, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "805:105": {"x": 840, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:105": {"x": 910, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:105": {"x": 980, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "1015:105": {"x": 1050, "y": 140, "left": false, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "1085:105": {"x": 1120, "y": 140, "left": true, "right": false, "bottom": false, "top": true, "window": true, "door": false}, "1155:105": {"x": 1190, "y": 140, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:105": {"x": 1260, "y": 140, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "-35:175": null, "35:175": {"x": 70, "y": 210, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "105:175": {"x": 140, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:175": {"x": 210, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:175": {"x": 280, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:175": {"x": 350, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:175": {"x": 420, "y": 210, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "455:175": {"x": 490, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:175": {"x": 560, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "595:175": {"x": 630, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:175": {"x": 700, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:175": {"x": 770, "y": 210, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "805:175": {"x": 840, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:175": {"x": 910, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:175": {"x": 980, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:175": {"x": 1050, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:175": {"x": 1120, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:175": {"x": 1190, "y": 210, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:175": {"x": 1260, "y": 210, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "-35:245": null, "35:245": {"x": 70, "y": 280, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "105:245": {"x": 140, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:245": {"x": 210, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:245": {"x": 280, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:245": {"x": 350, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:245": {"x": 420, "y": 280, "left": true, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "455:245": {"x": 490, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:245": {"x": 560, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "595:245": {"x": 630, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:245": {"x": 700, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:245": {"x": 770, "y": 280, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "805:245": {"x": 840, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:245": {"x": 910, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:245": {"x": 980, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:245": {"x": 1050, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:245": {"x": 1120, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:245": {"x": 1190, "y": 280, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:245": {"x": 1260, "y": 280, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "-35:315": null, "35:315": {"x": 70, "y": 350, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "105:315": {"x": 140, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:315": {"x": 210, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "245:315": {"x": 280, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "315:315": {"x": 350, "y": 350, "left": false, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "385:315": {"x": 420, "y": 350, "left": true, "right": false, "bottom": false, "top": true, "window": false, "door": false}, "455:315": {"x": 490, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:315": {"x": 560, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "595:315": {"x": 630, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:315": {"x": 700, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:315": {"x": 770, "y": 350, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "805:315": {"x": 840, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:315": {"x": 910, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:315": {"x": 980, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:315": {"x": 1050, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:315": {"x": 1120, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:315": {"x": 1190, "y": 350, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "1225:315": {"x": 1260, "y": 350, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "-35:385": null, "35:385": {"x": 70, "y": 420, "left": false, "right": true, "bottom": true, "top": true, "window": false, "door": false}, "105:385": {"x": 140, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "175:385": {"x": 210, "y": 420, "left": false, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "245:385": {"x": 280, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "315:385": {"x": 350, "y": 420, "left": true, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "385:385": {"x": 420, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "455:385": {"x": 490, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "525:385": {"x": 560, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "595:385": {"x": 630, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "665:385": {"x": 700, "y": 420, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "735:385": {"x": 770, "y": 420, "left": true, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "805:385": {"x": 840, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:385": {"x": 910, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:385": {"x": 980, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:385": {"x": 1050, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:385": {"x": 1120, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:385": {"x": 1190, "y": 420, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:385": {"x": 1260, "y": 420, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "-35:455": null, "35:455": {"x": 70, "y": 490, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": true}, "105:455": {"x": 140, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "175:455": {"x": 210, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:455": {"x": 280, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:455": {"x": 350, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:455": {"x": 420, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:455": {"x": 490, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:455": {"x": 560, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "595:455": {"x": 630, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:455": {"x": 700, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:455": {"x": 770, "y": 490, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": true}, "805:455": {"x": 840, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:455": {"x": 910, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:455": {"x": 980, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:455": {"x": 1050, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:455": {"x": 1120, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:455": {"x": 1190, "y": 490, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:455": {"x": 1260, "y": 490, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "-35:525": null, "35:525": {"x": 70, "y": 560, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": true}, "105:525": {"x": 140, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "175:525": {"x": 210, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "245:525": {"x": 280, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:525": {"x": 350, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:525": {"x": 420, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:525": {"x": 490, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:525": {"x": 560, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "595:525": {"x": 630, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:525": {"x": 700, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:525": {"x": 770, "y": 560, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": true}, "805:525": {"x": 840, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "875:525": {"x": 910, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:525": {"x": 980, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:525": {"x": 1050, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:525": {"x": 1120, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:525": {"x": 1190, "y": 560, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:525": {"x": 1260, "y": 560, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "-35:595": null, "35:595": {"x": 70, "y": 630, "left": false, "right": true, "bottom": true, "top": true, "window": false, "door": false}, "105:595": {"x": 140, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "175:595": {"x": 210, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "245:595": {"x": 280, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "315:595": {"x": 350, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "385:595": {"x": 420, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "455:595": {"x": 490, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "525:595": {"x": 560, "y": 630, "left": true, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "595:595": {"x": 630, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": true}, "665:595": {"x": 700, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "735:595": {"x": 770, "y": 630, "left": true, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "805:595": {"x": 840, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "875:595": {"x": 910, "y": 630, "left": true, "right": true, "bottom": true, "top": false, "window": false, "door": false}, "945:595": {"x": 980, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "1015:595": {"x": 1050, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "1085:595": {"x": 1120, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "1155:595": {"x": 1190, "y": 630, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "1225:595": {"x": 1260, "y": 630, "left": true, "right": false, "bottom": false, "top": true, "window": false, "door": false}, "-35:665": null, "35:665": {"x": 70, "y": 700, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "105:665": {"x": 140, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:665": {"x": 210, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "245:665": {"x": 280, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "315:665": {"x": 350, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "385:665": {"x": 420, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:665": {"x": 490, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:665": {"x": 560, "y": 700, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "595:665": {"x": 630, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": true}, "665:665": {"x": 700, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:665": {"x": 770, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "805:665": {"x": 840, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:665": {"x": 910, "y": 700, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "945:665": {"x": 980, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:665": {"x": 1050, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:665": {"x": 1120, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "1155:665": {"x": 1190, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:665": {"x": 1260, "y": 700, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:735": null, "35:735": {"x": 70, "y": 770, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "105:735": {"x": 140, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:735": {"x": 210, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:735": {"x": 280, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:735": {"x": 350, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:735": {"x": 420, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:735": {"x": 490, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:735": {"x": 560, "y": 770, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "595:735": {"x": 630, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:735": {"x": 700, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:735": {"x": 770, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "805:735": {"x": 840, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:735": {"x": 910, "y": 770, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "945:735": {"x": 980, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:735": {"x": 1050, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:735": {"x": 1120, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:735": {"x": 1190, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:735": {"x": 1260, "y": 770, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:805": null, "35:805": {"x": 70, "y": 840, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "105:805": {"x": 140, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:805": {"x": 210, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:805": {"x": 280, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:805": {"x": 350, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:805": {"x": 420, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:805": {"x": 490, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:805": {"x": 560, "y": 840, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "595:805": {"x": 630, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:805": {"x": 700, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:805": {"x": 770, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "805:805": {"x": 840, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:805": {"x": 910, "y": 840, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "945:805": {"x": 980, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:805": {"x": 1050, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:805": {"x": 1120, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:805": {"x": 1190, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:805": {"x": 1260, "y": 840, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:875": null, "35:875": {"x": 70, "y": 910, "left": false, "right": false, "bottom": true, "top": true, "window": true, "door": false}, "105:875": {"x": 140, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:875": {"x": 210, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:875": {"x": 280, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:875": {"x": 350, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:875": {"x": 420, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:875": {"x": 490, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:875": {"x": 560, "y": 910, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "595:875": {"x": 630, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:875": {"x": 700, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:875": {"x": 770, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "805:875": {"x": 840, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:875": {"x": 910, "y": 910, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "945:875": {"x": 980, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:875": {"x": 1050, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:875": {"x": 1120, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:875": {"x": 1190, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:875": {"x": 1260, "y": 910, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:945": null, "35:945": {"x": 70, "y": 980, "left": false, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "105:945": {"x": 140, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:945": {"x": 210, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "245:945": {"x": 280, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:945": {"x": 350, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:945": {"x": 420, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:945": {"x": 490, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:945": {"x": 560, "y": 980, "left": true, "right": false, "bottom": true, "top": true, "window": false, "door": false}, "595:945": {"x": 630, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:945": {"x": 700, "y": 980, "left": false, "right": true, "bottom": true, "top": false, "window": true, "door": false}, "735:945": {"x": 770, "y": 980, "left": true, "right": false, "bottom": true, "top": false, "window": true, "door": false}, "805:945": {"x": 840, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:945": {"x": 910, "y": 980, "left": false, "right": true, "bottom": true, "top": true, "window": false, "door": false}, "945:945": {"x": 980, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:945": {"x": 1050, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:945": {"x": 1120, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:945": {"x": 1190, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:945": {"x": 1260, "y": 980, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:1015": null, "35:1015": {"x": 70, "y": 1050, "left": false, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "105:1015": {"x": 140, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "175:1015": {"x": 210, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "245:1015": {"x": 280, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": true, "door": false}, "315:1015": {"x": 350, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "385:1015": {"x": 420, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "455:1015": {"x": 490, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "525:1015": {"x": 560, "y": 1050, "left": true, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "595:1015": {"x": 630, "y": 1050, "left": true, "right": true, "bottom": false, "top": false, "window": false, "door": false}, "665:1015": {"x": 700, "y": 1050, "left": true, "right": false, "bottom": false, "top": true, "window": true, "door": false}, "735:1015": {"x": 770, "y": 1050, "left": false, "right": true, "bottom": false, "top": true, "window": true, "door": false}, "805:1015": {"x": 840, "y": 1050, "left": true, "right": true, "bottom": false, "top": true, "window": false, "door": false}, "875:1015": {"x": 910, "y": 1050, "left": true, "right": false, "bottom": false, "top": true, "window": false, "door": false}, "945:1015": {"x": 980, "y": 1050, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:1015": {"x": 1050, "y": 1050, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:1015": {"x": 1120, "y": 1050, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:1015": {"x": 1190, "y": 1050, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:1015": {"x": 1260, "y": 1050, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "-35:1085": null, "35:1085": {"x": 70, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "105:1085": {"x": 140, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "175:1085": {"x": 210, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": true, "door": false}, "245:1085": {"x": 280, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "315:1085": {"x": 350, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "385:1085": {"x": 420, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "455:1085": {"x": 490, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "525:1085": {"x": 560, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "595:1085": {"x": 630, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "665:1085": {"x": 700, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "735:1085": {"x": 770, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "805:1085": {"x": 840, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "875:1085": {"x": 910, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "945:1085": {"x": 980, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1015:1085": {"x": 1050, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1085:1085": {"x": 1120, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1155:1085": {"x": 1190, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}, "1225:1085": {"x": 1260, "y": 1120, "left": false, "right": false, "bottom": false, "top": false, "window": false, "door": false}}')
    
    # print(jsonpickle.encode(mastergrid,unpicklable=False))
    # print(mastergrid)

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
