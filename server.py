from http.server import BaseHTTPRequestHandler,HTTPServer
import inspect


import jsonpickle
from APIResponse import Wall

from data import getData
from config import CONFIG
from draw import draw

def scale(walls:list[Wall],s:float):
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
                scale(walls,1.5)
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
