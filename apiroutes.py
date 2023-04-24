import os

API = {
    "GET":{},
    "POST":{},
}

def traversePath(path,debug=False,fileDebug=False):
    dir = os.listdir(path)
    if "__init__.py" not in dir:
        open(f"{path}/__init__.py", 'a').close()
    for item in dir:
        if not item.startswith("__"):
            newPath = f"{path}/{item}"
            cleanPath = path.replace("./routes","")
            if item[-3:]==".py":
                if item=="get.py":
                    pack = newPath[2:-3].replace("/",".")
                    imp = 'from ' + pack + " import GET"
                    if debug:
                        print(f"[API::ADD] [GET] {newPath if fileDebug else cleanPath}")
                    exec(imp)
                    exec('API["GET"][cleanPath]=GET')
                if item=="post.py":
                    pack = newPath[2:-3].replace("/",".")
                    imp = 'from ' + pack + " import POST"
                    if debug:
                        print(f"[API::ADD] [POST] {newPath if fileDebug else cleanPath}")
                    exec(imp)
                    exec('API["POST"][cleanPath]=POST')
            else:
                traversePath(newPath,debug)


def loadDynamicAPI(debug=False,fileDebug=True):
    traversePath("./routes",debug,fileDebug)
    return API

if __name__ == "__main__":
    api = loadDynamicAPI(True)
    print(api)
