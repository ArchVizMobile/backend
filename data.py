import json
import random
from config import CONFIG

def getData():
    w = CONFIG.getIMAGE_WIDTH()
    h = CONFIG.getIMAGE_HEIGHT()

    wall_width = CONFIG.getWALL_WIDTH()
    wall_width_half = wall_width/2


    rooms = [
        [[100,100,True,"#000000"]],
    ]
    vertical_roomz_count = CONFIG.getVERTICAL_ROOMZ_COUNT()
    horizohntahl_roomz_count = CONFIG.getHORIZOHNTAHL_ROOMZ_COUNT()

    for a in range(horizohntahl_roomz_count):
        if random.random() > 0.3:
            min = round(rooms[0][len(rooms[0])-1][0]+(h/(horizohntahl_roomz_count*2)))
            max = round(rooms[0][len(rooms[0])-1][0]+(h/horizohntahl_roomz_count))
            rooms[0].append([
                int(random.randrange(min,max)),
                rooms[0][0][1],
                True,
                "#000000"
            ])

    for n in range(vertical_roomz_count):
        last_room = rooms[len(rooms)-1][0]
        min = round(last_room[1]+(h/(vertical_roomz_count*2)))
        max = round(last_room[1]+(h/vertical_roomz_count))
        r = [[
                last_room[0],
                int(random.randrange(min,max)),
                True,
                "#000000"
            ]]
        for a in range(horizohntahl_roomz_count):
            if random.random() > 0.3:
                min = round(r[len(r)-1][0]+(h/(horizohntahl_roomz_count*2)))
                max = round(r[len(r)-1][0]+(h/horizohntahl_roomz_count))
                r.append([
                    int(random.randrange(min,max)),
                    r[len(r)-1][1],
                    True,
                    "#000000"
                ])
        rooms.append(r)

    for idx,y in enumerate(rooms):
        if idx<len(rooms)-1:
            for x in y:
                if x[2]:
                    rooms[idx+1].append([x[0],rooms[idx+1][0][1],False,"#000000"])

    last_y = int(rooms[len(rooms)-1][0][1]+100)
    if last_y > h-10:
        last_y = h - 10

    r = []
    for idx,x in enumerate(rooms[len(rooms)-1]):
        if x[2]:
            # print(x)
            r.append([x[0],last_y,False,"#000000"])
    rooms.append(r)

    # print(f'vertical_roomz_count= {vertical_roomz_count} ; horizohntahl_roomz_count= {horizohntahl_roomz_count} ; rooms= {rooms}')

    for idx,row in enumerate(rooms):
        if len(row) == 1:
            print(f"deleting row {row}")
            del rooms[idx][0]

    for y in rooms:
        y.sort(key = lambda x: x[0])

    # rooms = [[[100, 100, True, '#000000'], [294, 100, True, '#000000'], [563, 100, True, '#000000']], [[100, 415, True, '#000000'], [100, 415, False, '#000000'], [294, 415, False, '#000000'], [398, 415, True, '#000000'], [563, 415, False, '#000000'], [592, 415, True, '#000000']], [[100, 750, True, '#000000'], [100, 750, False, '#000000'], [398, 750, False, '#000000'], [446, 750, True, '#000000'], [592, 750, False, '#000000'], [738, 750, True, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 1070, False, '#000000'], [444, 1070, False, '#000000'], [659, 1070, False, '#000000']]]
    # print(rooms)

    # good example
    # rooms = [[[100, 100, True, '#000000'], [455, 100, True, '#000000'], [813, 100, True, '#000000']], [[100, 444, True, '#000000'], [100, 444, False, '#000000'], [432, 444, True, '#000000'], [455, 444, False, '#000000'], [656, 444, True, '#000000'], [813, 444, False, '#000000']], [[100, 758, True, '#000000'], [100, 758, False, '#000000'], [396, 758, True, '#000000'], [432, 758, False, '#000000'], [610, 758, True, '#000000'], [656, 758, False, '#000000']], [[100, 1125, True, '#000000'], [100, 1125, False, '#000000'], [396, 1125, False, '#000000'], [484, 1125, True, '#000000'], [610, 1125, False, '#000000']], [[100, 1190, False, '#000000'], [484, 1190, False, '#000000']]]

    # bad example
    rooms = [[[100, 100, True, '#000000'], [491, 100, True, '#000000'], [880, 100, True, '#000000']], [[100, 385, True, '#000000'], [100, 385, False, '#000000'], [474, 385, True, '#000000'], [491, 385, False, '#000000'], [696, 385, True, '#000000'], [880, 385, False, '#000000']], [[100, 733, True, '#000000'], [100, 733, False, '#000000'], [376, 733, True, '#000000'], [474, 733, False, '#000000'], [696, 733, False, '#000000'], [755, 733, True, '#000000']], [[100, 991, True, '#000000'], [100, 991, False, '#000000'], [331, 991, True, '#000000'], [376, 991, False, '#000000'], [600, 991, True, '#000000'], [755, 991, False, '#000000']], [[100, 1091, False, '#000000'], [331, 1091, False, '#000000'], [600, 1091, False, '#000000']]]

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
    

    wallsobj = []

    for idx,wall in enumerate(wallsarr):
        wallsobj.append({
            "from": {
                "x": int(wall[0][0][0]),
                "y": int(wall[0][0][1])
            },
            "to": {
                "x": int(wall[0][1][0]),
                "y": int(wall[0][1][1])
            },
            "isHorizontal": wall[1],
            "isOuterWall": wall[2],
            "windows":[],
            "doors":[],
        })
    
    outerwalls = []
    for idx,wall in enumerate(wallsobj):
        if wall["isOuterWall"]:
            outerwalls.append({"idx":idx,"wall":wall})

    # for n in range(int(random.random()*3)):
    for n in range(10):
        idx = random.randrange(0,len(outerwalls))
        o = wallsobj[outerwalls[idx]["idx"]]
        # top left, right, bottom right, left
        openSide = [False,False,False,False]
        openSide[int(random.random()*4)] = True

        doorWidth = int(random.randrange(80,120))

        if not o["isHorizontal"] and len(o["doors"])==0 and o["to"]["y"]-o["from"]["y"] > doorWidth*2:
            o["doors"].append({
                "from": 50,
                "to": doorWidth + 50,
                "hinge":openSide,
                "width":doorWidth
            })

        if o["isHorizontal"] and len(o["doors"])==0 and o["to"]["x"]-o["from"]["x"] > doorWidth*2:
            o["doors"].append({
                "from": 50,
                "to": doorWidth + 50,
                "hinge":openSide,
                "width":doorWidth
            })

    # print(outerwalls)

    return wallsobj,joints,wallsarr
