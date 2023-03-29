import random
from config import CONFIG

def createHorizontalWall(xbefore:int,ybefore:int):
    min = round(xbefore + 200)
    max = round(xbefore + 500)
    return {
        "x": int(random.randrange(min,max)),
        "y": ybefore,
        "generated": True
    }

def createVerticalWall(xbefore:int,ybefore:int):
    min = round(ybefore + 200)
    max = round(ybefore + 500)
    return {
        "x": xbefore,
        "y": int(random.randrange(min,max)),
        "generated": True
    }

def rngWall():
    return random.random() > 0.3

def generateCorners():
    rooms = [
        [{"x":100,"y":100,"generated":True}],
    ]
    vertical_roomz_count = int(random.randrange(2,5))
    horizohntahl_roomz_count = int(random.randrange(2,5))

    # Top Wall Generation
    for _ in range(horizohntahl_roomz_count):
        if rngWall():
            rooms[0].append(createHorizontalWall(rooms[0][len(rooms[0])-1]["x"],rooms[0][0]["y"]))

    # All Horizontal Lines and the most left wall
    for _ in range(vertical_roomz_count):
        last_room = rooms[len(rooms)-1][0]
        r = [createVerticalWall(last_room["x"],last_room["y"])]

        for _ in range(horizohntahl_roomz_count):
            if rngWall():
                r.append(createHorizontalWall(r[len(r)-1]["x"],r[len(r)-1]["y"]))

        # forcing at least one room
        if len(r) == 1:
            r.append(createHorizontalWall(r[len(r)-1]["x"],r[len(r)-1]["y"]))

        # forcing at least two rooms
        if len(r) == 2:
            r.append(createHorizontalWall(r[len(r)-1]["x"],r[len(r)-1]["y"]))
        rooms.append(r)

    # Generate Vertical Walls
    for idx,y in enumerate(rooms):
        if idx<len(rooms)-1:
            for x in y:
                if x["generated"]:
                    rooms[idx+1].append({
                        "x":x["x"],
                        "y":rooms[idx+1][0]["y"],
                        "generated":False
                    })

    last_y = int(rooms[len(rooms)-1][0]["y"]+200)

    # Copying nodes to make sure every room has an end
    r = []
    for idx,x in enumerate(rooms[len(rooms)-1]):
        if x["generated"]:
            r.append({
                "x":x["x"],
                "y":last_y,
                "generated":False
            })
    rooms.append(r)

    for y in rooms:
        y.sort(key = lambda x: x["x"])
        
    return rooms
