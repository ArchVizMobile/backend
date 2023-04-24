from datetime import datetime

import jsonpickle
from data import getData
from draw import draw

def GET(self,dbCollection,search):
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
            for item in w.features:
                item.fromPosition = int(item.fromPosition * s)
                item.toPosition = int(item.toPosition * s)
                item.z = int(item.z * s)
                item.height = int(item.height * s)
                item.hinge = int(item.hinge * s)

        for r in rooms:
            r.fromPosition.x = int(r.fromPosition.x * s)
            r.fromPosition.y = int(r.fromPosition.y * s)
            r.toPosition.x = int(r.toPosition.x * s)
            r.toPosition.y = int(r.toPosition.y * s)

        #wallsobj,junctions,wallsarr = getData()
        # draw(junctions,walls,rooms)
    except Exception as e:
        print(e)
        walls,junctions,rooms = "no","no","no"
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    id = ""
    data = {
        "success": walls!="no",
        "name": f"Generated Floorplan from {dt_string}",
        "walls": walls,
        "junctions": junctions,
        "rooms": rooms,
        "scale": s,
    }
    json = jsonpickle.encode(data, unpicklable=False)
    if walls!="no":
        id = dbCollection.insert_one(jsonpickle.decode(json))
        data["_id"] = str(id.inserted_id)

    return data