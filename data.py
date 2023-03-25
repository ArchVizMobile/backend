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
        if random.random() > 0.5:
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

    rooms = [[[100, 100, True, '#000000'], [294, 100, True, '#000000'], [563, 100, True, '#000000']], [[100, 415, True, '#000000'], [100, 415, False, '#000000'], [294, 415, False, '#000000'], [398, 415, True, '#000000'], [563, 415, False, '#000000'], [592, 415, True, '#000000']], [[100, 750, True, '#000000'], [100, 750, False, '#000000'], [398, 750, False, '#000000'], [446, 750, True, '#000000'], [592, 750, False, '#000000'], [738, 750, True, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 1070, False, '#000000'], [444, 1070, False, '#000000'], [659, 1070, False, '#000000']]]

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
            joints.append({"left":x[0],"top":x[1],"corner":{"top":False,"left":False,"bottom":False,"right":False}})

    for idx,room in enumerate(joints):
        for idx1,room1 in enumerate(joints):
            if idx!=idx1:
                if room["left"] > room1["left"]:
                    room["corner"]["left"]=True
                if room["left"] < room1["left"]:
                    room["corner"]["right"]=True
                if room["top"] > room1["top"]:
                    room["corner"]["top"]=True
                if room["top"] < room1["top"]:
                    room["corner"]["bottom"]=True

    wallsarr = []

    for yidx,y in enumerate(rooms):
        for xidx,x in enumerate(y):
            if xidx+1 < len(y):
                outline = yidx==0 or yidx==len(rooms)-1
                wall = [[
                    [x[0]-wall_width_half,x[1]+wall_width_half],
                    [y[xidx+1][0]+wall_width_half,y[xidx+1][1]-wall_width_half],
                ],True,outline]
                wallsarr.append(wall)
            if yidx+1 < len(rooms):
                for tidx,t in enumerate(rooms[yidx+1]):
                    if x[0] == t[0] and x[1] != t[1]:
                        outline = tidx == 0 or tidx==len(rooms[yidx+1])-1
                        wall = [[
                            [x[0]+wall_width_half,x[1]-wall_width_half],
                            [t[0]-wall_width_half,t[1]+wall_width_half],
                        ],False,outline]
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
        })

    return wallsobj,joints,wallsarr
