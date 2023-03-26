import random
from typing import List
from APIResponse import APIResponse, Door, Position, SimplePosition, Wall, Window
from config import CONFIG
from generateCorners import generateCorners

# a <= x <= b
def between(a,x,b):
    return a <= x and x <= b

def betweenPosition(pos,item):
    return between(item.fromPosition,pos,item.toPosition)

def checkIntersecting(arr:List[SimplePosition],fr:int,to:int):
    for item in arr:
        currentInItem = betweenPosition(fr,item) or \
                        betweenPosition(to,item)
        
        itemInCurrent = between(item.fromPosition,fr,item.toPosition) or \
                        between(item.fromPosition,to,item.toPosition)
        if currentInItem or itemInCurrent:
            return True
    return False


def getData():
    response = APIResponse(success=False,junctions=[],walls=[])

    rooms = generateCorners()

    wall_width = CONFIG.getWALL_WIDTH()
    wall_width_half = wall_width/2

    rooms = [[[100, 100, True, '#000000'], [294, 100, True, '#000000'], [563, 100, True, '#000000']], [[100, 415, True, '#000000'], [100, 415, False, '#000000'], [294, 415, False, '#000000'], [398, 415, True, '#000000'], [563, 415, False, '#000000'], [592, 415, True, '#000000']], [[100, 750, True, '#000000'], [100, 750, False, '#000000'], [398, 750, False, '#000000'], [446, 750, True, '#000000'], [592, 750, False, '#000000'], [738, 750, True, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 1070, False, '#000000'], [444, 1070, False, '#000000'], [659, 1070, False, '#000000']]]
    # print(rooms)

    # good example
    # rooms = [[[100, 100, True, '#000000'], [455, 100, True, '#000000'], [813, 100, True, '#000000']], [[100, 444, True, '#000000'], [100, 444, False, '#000000'], [432, 444, True, '#000000'], [455, 444, False, '#000000'], [656, 444, True, '#000000'], [813, 444, False, '#000000']], [[100, 758, True, '#000000'], [100, 758, False, '#000000'], [396, 758, True, '#000000'], [432, 758, False, '#000000'], [610, 758, True, '#000000'], [656, 758, False, '#000000']], [[100, 1125, True, '#000000'], [100, 1125, False, '#000000'], [396, 1125, False, '#000000'], [484, 1125, True, '#000000'], [610, 1125, False, '#000000']], [[100, 1190, False, '#000000'], [484, 1190, False, '#000000']]]

    # bad example
    # rooms = [[[100, 100, True, '#000000'], [491, 100, True, '#000000'], [880, 100, True, '#000000']], [[100, 385, True, '#000000'], [100, 385, False, '#000000'], [474, 385, True, '#000000'], [491, 385, False, '#000000'], [696, 385, True, '#000000'], [880, 385, False, '#000000']], [[100, 733, True, '#000000'], [100, 733, False, '#000000'], [376, 733, True, '#000000'], [474, 733, False, '#000000'], [696, 733, False, '#000000'], [755, 733, True, '#000000']], [[100, 991, True, '#000000'], [100, 991, False, '#000000'], [331, 991, True, '#000000'], [376, 991, False, '#000000'], [600, 991, True, '#000000'], [755, 991, False, '#000000']], [[100, 1091, False, '#000000'], [331, 1091, False, '#000000'], [600, 1091, False, '#000000']]]

    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            room1[0] = room1[0] - (room1[0] % 20)
            room1[1] = room1[1] - (room1[1] % 20)

    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            for idx2,room2 in enumerate(room):
                if idx1!=idx2 and room1[0]==room2[0] and room1[1]==room2[1]:
                    del room[idx2]
    

    joints = []
    for idx,y in enumerate(rooms):
        for xidx,x in enumerate(y):
            joints.append({
                "left":x[0],
                "top":x[1],
                "outerwall": False,
                "corner":{
                    "top":None,
                    "left":None,
                    "bottom":None,
                    "right":None
                },
                "targetIsOuterwall":{
                    "top":False,
                    "left":False,
                    "bottom":False,
                    "right":False
                }})
    
    for idx,room in enumerate(joints):
        for idx1,room1 in enumerate(joints):
            # if idx!=idx1:
                if room["left"] > room1["left"] and room["top"]==room1["top"] and (room["corner"]["left"]==None or room["left"] > joints[room["corner"]["left"]]["left"]):
                    room["corner"]["left"]=idx1

                if room["left"] < room1["left"] and room["top"]==room1["top"] and (room["corner"]["right"]==None or room["left"] > joints[room["corner"]["right"]]["left"]):
                    room["corner"]["right"]=idx1

                if room["top"] > room1["top"] and room["left"]==room1["left"] and (room["corner"]["top"]==None or room["top"] > joints[room["corner"]["top"]]["top"]):
                    room["corner"]["top"]=idx1

                if room["top"] < room1["top"] and room["left"]==room1["left"] and (room["corner"]["bottom"]==None or room["top"] > joints[room["corner"]["bottom"]]["top"]):
                    room["corner"]["bottom"]=idx1


    def traverse(idx,move):
        joints[idx]["outerwall"] = True
        current = joints[idx]
        corner = current["corner"]
        if move=="right":
            if corner["right"]!=None and not joints[corner["right"]]["outerwall"]:
                traverse(corner["right"],"right")
            elif corner["bottom"]!=None and not joints[corner["bottom"]]["outerwall"]:
                traverse(corner["bottom"],"bottom")
            elif corner["top"]!=None and not joints[corner["top"]]["outerwall"]:
                traverse(corner["top"],"top")
            elif corner["left"]!=None and not joints[corner["left"]]["outerwall"]:
                traverse(corner["left"],"left")

        if move=="bottom":
            if corner["bottom"]!=None and not joints[corner["bottom"]]["outerwall"]:
                traverse(corner["bottom"],"bottom")
            elif corner["right"]!=None and not joints[corner["right"]]["outerwall"]:
                traverse(corner["right"],"right")
            elif corner["top"]!=None and not joints[corner["top"]]["outerwall"]:
                traverse(corner["top"],"top")
            elif corner["left"]!=None and not joints[corner["left"]]["outerwall"]:
                traverse(corner["left"],"left")

        if move=="left":
            if corner["bottom"]!=None and not joints[corner["bottom"]]["outerwall"]:
                traverse(corner["bottom"],"bottom")
            elif corner["left"]!=None and not joints[corner["left"]]["outerwall"]:
                traverse(corner["left"],"left")
            elif corner["right"]!=None and not joints[corner["right"]]["outerwall"]:
                traverse(corner["right"],"right")
            elif corner["top"]!=None and not joints[corner["top"]]["outerwall"]:
                traverse(corner["top"],"top")
            

        if move=="top":
            if idx!=0:
                traverse(corner["top"],"top")
            

    traverse(0,"right")

    for idx,joint in enumerate(joints):
        if joints[idx]["corner"]["top"]!=None:
            joints[idx]["targetIsOuterwall"]["top"] = joints[joints[idx]["corner"]["top"]]["outerwall"]
        if joints[idx]["corner"]["left"]!=None:
            joints[idx]["targetIsOuterwall"]["left"] = joints[joints[idx]["corner"]["left"]]["outerwall"]
        if joints[idx]["corner"]["bottom"]!=None:
            joints[idx]["targetIsOuterwall"]["bottom"] = joints[joints[idx]["corner"]["bottom"]]["outerwall"]
        if joints[idx]["corner"]["right"]!=None:
            joints[idx]["targetIsOuterwall"]["right"] = joints[joints[idx]["corner"]["right"]]["outerwall"]

    # print(json.dumps(joints,indent=2))

    wallsarr = []

    for idx,x in enumerate(joints):
        if x["corner"]["right"]:
            wall = [[
                [x["left"]+wall_width_half,x["top"]-wall_width_half],
                [joints[x["corner"]["right"]]["left"]-wall_width_half,joints[x["corner"]["right"]]["top"]+wall_width_half],
            ],True,x["targetIsOuterwall"]["right"] and x["outerwall"]]
            wallsarr.append(wall)
            
        if x["corner"]["bottom"]:
            wall = [[
                [x["left"]+wall_width_half,x["top"]-wall_width_half],
                [joints[x["corner"]["bottom"]]["left"]-wall_width_half,joints[x["corner"]["bottom"]]["top"]+wall_width_half],
            ],False,x["targetIsOuterwall"]["bottom"] and x["outerwall"]]
            wallsarr.append(wall)
    

    wallsobj:List[Wall] = []

    for idx,wall in enumerate(wallsarr):
        wallsobj.append(Wall(
            fromPosition=Position(int(wall[0][0][0]),int(wall[0][0][1])),
            toPosition=Position(int(wall[0][1][0]),int(wall[0][1][1])),
            isHorizontal=wall[1],
            isOuterWall=wall[2],
            doors=[],
            windows=[]
        ))
    
    outerwalls = []
    innerwalls = []
    for idx,wall in enumerate(wallsobj):
        if wall.isOuterWall:
            outerwalls.append({"idx":idx,"wall":wall})
        else:
            innerwalls.append({"idx":idx,"wall":wall})

    # outer walls doors
    for _ in range(10):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            hinge = fromPosition if random.random() > 0.5 else toPosition
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.doors.append(Door(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default"
                ))

    # outer walls windows
    for _ in range(100):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.windows.append(Window(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    style = "default"
                ))

    # inner walls
    for wall in innerwalls:
        o:Wall = wallsobj[wall["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            hinge = fromPosition if random.random() > 0.5 else toPosition
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.doors.append(Door(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default"
                ))


    response.walls = wallsobj

    return wallsobj,joints,wallsarr
