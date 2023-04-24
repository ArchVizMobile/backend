from datetime import date
from http.server import BaseHTTPRequestHandler,HTTPServer
import io
import os
import re
from bson import ObjectId
import jsonpickle
from APIResponse import Wall
import typing

from data import getData
from config import CONFIG
from draw import draw, drawAndReturnFromDatabase

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
# print(f"mongodb://{CONFIG.getDB_HOST()}:{CONFIG.getDB_PORT()}/ -> CONFIG.getDB_DATABASE() -> floorplans")

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

        # params = self.path.split("?")[1]
        url = urlparse(self.path)
        path = url.path
        search = {}
        if url.query !="":
            for item in url.query.split("&"):
                key,value = item.split("=")
                search[key]=value
        # print(search)

        if path=="/image" and "id" in search:
            self.send_header('Content-type','image/jpeg')

            data = mycollection.find_one({"_id":ObjectId(search["id"])})

            im = drawAndReturnFromDatabase(data["junctions"],data["walls"],data["rooms"])
            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            self.wfile.write(img_byte_arr)
            return

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
        
        if self.path.endswith("/"):
            self.send_header('Content-type','application/json')
            ret = API["GET"][""](self,search={},dbCollection=mycollection)
            json = jsonpickle.encode(ret, unpicklable=False)

            self.wfile.write(json.encode())
            return
        if self.path.endswith("/dash.html"):
            self.send_header('Content-type','text/html')
            self.wfile.write(open('dash.html', 'rb'))
            return
        if self.path.endswith("/last.jpg"):
            self.send_header('Content-type','image/jpeg')
            with open("whh.jpg", 'rb') as file_handle:
                file = file_handle.read()
                return self.wfile.write(file)
            #self.wfile.write(open('./whh.jpg', 'rb'))
            return
        self.wfile.write("no".encode())


def run(server_class=HTTPServer, handler_class=Server, port=CONFIG.getSERVER_PORT()):
    server_address = (CONFIG.getWEB_HOST(), CONFIG.getWEB_PORT())
    httpd = server_class(server_address, handler_class)

    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    # getData()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
