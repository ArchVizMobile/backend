import random
from config import CONFIG

def generateCorners():
    
    w = CONFIG.getIMAGE_WIDTH()
    h = CONFIG.getIMAGE_HEIGHT()

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
        
    return rooms
