from http.server import BaseHTTPRequestHandler,HTTPServer
import json

from data import getData

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
