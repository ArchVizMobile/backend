import numpy as np
from PIL import Image, ImageDraw
import random
import time
from http.server import BaseHTTPRequestHandler,HTTPServer
import json

def getData():
    w, h = 1080, 1080
    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
    img1 = ImageDraw.Draw(im)

    wall_width = 0
    wall_width_half = wall_width/2


    rooms = [
        [[100,100,True,"#000000"]],
    ]
    vertical_roomz_count = 3 #int(random.random()*4+3)
    horizohntahl_roomz_count = 3 #int(random.random()*3+2)

    for a in range(horizohntahl_roomz_count):
        if random.random() > 0.5:
            rooms[0].append([
                int(random.randrange(rooms[0][len(rooms[0])-1][0]+(h/(horizohntahl_roomz_count*2)),rooms[0][len(rooms[0])-1][0]+(h/horizohntahl_roomz_count))),
                rooms[0][0][1],
                True,
                "#000000"
            ])

    for n in range(vertical_roomz_count):
        last_room = rooms[len(rooms)-1][0]
        r = [[
                last_room[0],
                int(random.randrange(last_room[1]+(h/(vertical_roomz_count*2)),last_room[1]+(h/vertical_roomz_count))),
                True,
                "#000000"
            ]]
        for a in range(horizohntahl_roomz_count):
            if random.random() > 0.3:
                r.append([
                    int(random.randrange(r[len(r)-1][0]+(h/(horizohntahl_roomz_count*2)),r[len(r)-1][0]+(h/horizohntahl_roomz_count))),
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
        # print(f"{len(row)} row {row}")
        if len(row) == 1:
            print(f"deleting row {row}")
            del rooms[idx][0]

    for y in rooms:
        y.sort(key = lambda x: x[0])

    # print(rooms)
    # rooms = [[[100, 100, True, '#000000'], [294, 100, True, '#000000'], [563, 100, True, '#000000']], [[100, 415, True, '#000000'], [100, 415, False, '#000000'], [294, 415, False, '#000000'], [398, 415, True, '#000000'], [563, 415, False, '#000000'], [592, 415, True, '#000000']], [[100, 750, True, '#000000'], [100, 750, False, '#000000'], [398, 750, False, '#000000'], [446, 750, True, '#000000'], [592, 750, False, '#000000'], [738, 750, True, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 982, True, '#000000'], [100, 982, False, '#000000'], [444, 982, True, '#000000'], [446, 982, False, '#000000'], [659, 982, True, '#000000'], [738, 982, False, '#000000']], [[100, 1070, False, '#000000'], [444, 1070, False, '#000000'], [659, 1070, False, '#000000']]]

    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            room1[0] = room1[0] - (room1[0] % 20)
            room1[1] = room1[1] - (room1[1] % 20)

    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            for idx2,room2 in enumerate(room):
                if idx1!=idx2 and room1[0]==room2[0] and room1[1]==room2[1]:
                    # print(f"deleting double {room2}")
                    del room[idx2]
            # if idx1!=idx and room == json.dumps(room1):
                # del room1
    

    roomz = []
    for idx,y in enumerate(rooms):
        for xidx,x in enumerate(y):
            roomz.append({"left":x[0],"top":x[1],"corner":{"top":False,"left":False,"bottom":False,"right":False}})

    for idx,room in enumerate(roomz):
        for idx1,room1 in enumerate(roomz):
            if idx!=idx1:
                if room["left"] > room1["left"]:
                    room["corner"]["left"]=True
                if room["left"] < room1["left"]:
                    room["corner"]["right"]=True
                if room["top"] > room1["top"]:
                    room["corner"]["top"]=True
                if room["top"] < room1["top"]:
                    room["corner"]["bottom"]=True
                # if room[0]

    walls = []

    for yidx,y in enumerate(rooms):
        for xidx,x in enumerate(y):
            # print(f"y={yidx} x={xidx}")
            if xidx+1 < len(y):
                outline = yidx==0 or yidx==len(rooms)-1
                wall = [[
                    [x[0]-wall_width_half,x[1]+wall_width_half],
                    [y[xidx+1][0]+wall_width_half,y[xidx+1][1]-wall_width_half],
                ],True,outline]
                walls.append(wall)
            if yidx+1 < len(rooms):
                for tidx,t in enumerate(rooms[yidx+1]):
                    if x[0] == t[0] and x[1] != t[1]:
                        outline = tidx == 0 or tidx==len(rooms[yidx+1])-1
                        wall = [[
                            [x[0]+wall_width_half,x[1]-wall_width_half],
                            [t[0]-wall_width_half,t[1]+wall_width_half],
                        ],False,outline]
                        walls.append(wall)

    # print(f"walls = {walls}")
    # print(f"rooms = {rooms}")

    returnwalls = []

    for idx,wall in enumerate(walls):
        fill = "#000"
        # print(wall)
        # if(wall[2]):
            # fill = "#f00"
        returnwalls.append({
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

    # filename = f"images/{time.time()}.jpg"
    # im.save(filename)
    # im.save("whh.jpg")
    # csv = "Index,sourceX,sourceY,targetX,targetY,isHorizontal\n"

    # for idx,wall in enumerate(walls):
    #     csv = csv+f"{idx+1},{wall[0][0][0]},{wall[0][0][1]},{wall[0][1][0]},{wall[0][1][1]}\n"
        # csv.append([idx,wall[0][0][0],wall[0][0][1],wall[0][1][0],wall[0][1][1]])
    # return csv
    return returnwalls,roomz
# for n in range(100):
    # run()
# run()

class Server(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    # GET sends back a Hello world message
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path.endswith("/"):
            try:
                walls,roomz = getData()
            except:
                walls = "no"
                roomz = "no"
            self.wfile.write(json.dumps({
                "success": walls!="no",
                "walls": walls,
                "roomz": roomz,
            }).encode())
            return
        if self.path.endswith("/dash.html"):
            self.wfile.write(open('dash.html', 'rb'))
            return
        self.wfile.write("no".encode())


def run(server_class=HTTPServer, handler_class=Server, port=1234):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    # getData()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
