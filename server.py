from datetime import date
from http.server import BaseHTTPRequestHandler,HTTPServer
import os
import re
from bson import ObjectId
import jsonpickle
from APIResponse import Wall
import typing

from data import getData
from config import CONFIG
from draw import draw

import pymongo
import random
import string
from datetime import datetime
from urllib.parse import  urlparse

from apiroutes import loadDynamicAPI
API = loadDynamicAPI(debug=True,fileDebug=False)

myclient = pymongo.MongoClient(f"mongodb://{CONFIG.getDB_HOST()}:{CONFIG.getDB_PORT()}/")
mydb = myclient[CONFIG.getDB_DATABASE()]
mycollection = mydb["floorplans"]

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

class Server(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

        path = self.path

        if path in API["POST"]:
            response = API["POST"][path](path)
            json = jsonpickle.encode(response, unpicklable=False)

            self.wfile.write(json.encode())
            return

    # GET sends back a Hello world message
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        #self.send_header('Content-type','text/html')
        self.end_headers()

        path = self.path.split("?")[0]
        # params = self.path.split("?")[1]
        url = urlparse(self.path)
        search = {}
        if url.query !="":
            for item in url.query.split("&"):
                key,value = item.split("=")
                search[key]=value
        # print(search)

        if path in API["GET"]:
            self.send_header('Content-type','application/json')
            # self.
            response = API["GET"][path](self,search=search,dbCollection=mycollection)
            json = jsonpickle.encode(response, unpicklable=False)

            self.wfile.write(json.encode())
            return

        if self.path.startswith("/get"):
            self.send_header('Content-type','application/json')
            search = {"_id":ObjectId(self.path.split("/")[2])}
            cnt = mycollection.count_documents(search)
            ret = {
                "success": False,
                "walls": [],
                "junctions": [],
                "rooms": [],
                "scale": -1,
            }

            if cnt > 0:
                lst = mycollection.find(search)
                ret = lst[0]
                ret["_id"] = str(ret["_id"])

            json = jsonpickle.encode(ret, unpicklable=False)

            self.wfile.write(json.encode())
            return
        # if self.path.endswith("/list"):
        #     self.send_header('Content-type','application/json')
        #     lst = []
        #     for item in mycollection.find():
        #         lst.append({
        #             "id": str(item.get('_id')),
        #             "name": item.get("name"),
        #             "image": "/image/"+str(item.get('_id'))
        #         })
        #         # lst.append((item.get('_id')))
        #     json = jsonpickle.encode({"success":True,"list":lst}, unpicklable=False)
        #     self.wfile.write(json.encode())
        #     return
        if self.path.endswith("/"):
            self.send_header('Content-type','application/json')
            s = 1.5
            try:
                walls,junctions,rooms = getData()
                # scale(walls,1.5)
                
                for w in walls:
                    w.depth = int(w.depth * s)
                    w.height = int(w.height * s)
                    w.fromPosition.x = int(w.fromPosition.x * s)
                    w.fromPosition.y = int(w.fromPosition.y * s)
                    w.toPosition.x = int(w.toPosition.x * s)
                    w.toPosition.y = int(w.toPosition.y * s)
                    for item in w.doors:
                        item.fromPosition = int(item.fromPosition * s)
                        item.toPosition = int(item.toPosition * s)
                        item.z = int(item.z * s)
                        item.height = int(item.height * s)
                        item.hinge = int(item.hinge * s)

                    for item in w.windows:
                        item.fromPosition = int(item.fromPosition * s)
                        item.toPosition = int(item.toPosition * s)
                        item.z = int(item.z * s)
                        item.height = int(item.height * s)

                for r in rooms:
                    r.fromPosition.x = int(r.fromPosition.x * s)
                    r.fromPosition.y = int(r.fromPosition.y * s)
                    r.toPosition.x = int(r.toPosition.x * s)
                    r.toPosition.y = int(r.toPosition.y * s)

                #wallsobj,junctions,wallsarr = getData()
                draw(junctions,walls,rooms)
            except Exception as e:
                print(e)
                walls,junctions,rooms = "no","no","no"
            now = datetime.now()
            dt_string = now.strftime("%d.%m.%Y %H:%M:%S")

            data = {
                "success": walls!="no",
                "name": f"Generated Floorplan from {dt_string}",
                "walls": walls,
                "junctions": junctions,
                "rooms": rooms,
                "scale": s,
            }
            json = jsonpickle.encode(data, unpicklable=False)
            if data["success"]:
                x = mycollection.insert_one(jsonpickle.decode(json))
            self.wfile.write(json.encode())
            return
        if self.path.endswith("/dash.html"):
            self.send_header('Content-type','text/html')
            self.wfile.write(open('dash.html', 'rb'))
            return
        if self.path.endswith("/last.jpg"):
            self.send_header('Content-type','image/jpeg')
            with open("whh.jpg", 'rb') as file_handle:
                return self.wfile.write(file_handle.read())
            #self.wfile.write(open('./whh.jpg', 'rb'))
            return
        self.wfile.write("no".encode())


def run(server_class=HTTPServer, handler_class=Server, port=CONFIG.getSERVER_PORT()):
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
