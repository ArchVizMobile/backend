import random
from bson import ObjectId

from config import CONFIG

def GET(self,dbCollection,search):
    lst = []
    for item in dbCollection.find():
        lst.append({
            "id": str(item.get('_id')),
            "name": item.get("name"),
            "image": f"{CONFIG.getWEB_PROTOCOL()}://{CONFIG.getWEB_HOST()}:{CONFIG.getWEB_PORT()}/image?id="+str(item.get('_id')),
            "number_of_rooms": random.randint(0,1337),
            "qm": random.randint(0,42),
            "floors": random.randint(0,69),
            "vendor": ["self","hvh"][random.randint(0,1)],
            "background": ["city","land"][random.randint(0,1)],
            "facts": "lelele rofl keepo",
        })
    return {"success":True,"list":lst}
