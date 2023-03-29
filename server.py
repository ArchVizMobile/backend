from http.server import BaseHTTPRequestHandler,HTTPServer
import json


import jsonpickle

from data import getData
from config import CONFIG
from draw import draw

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
        #self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path.endswith("/"):
            self.send_header('Content-type','application/json')
            try:
                walls,junctions = getData()
                #wallsobj,junctions,wallsarr = getData()
                draw(junctions,walls)
            except Exception as e:
                print(e)
                walls,junctions = "no","no"
            self.wfile.write(jsonpickle.encode({
                "success": walls!="no",
                "walls": walls,
                "junctions": junctions,
            }, unpicklable=False).encode())
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
