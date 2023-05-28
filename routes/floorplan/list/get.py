from bson import ObjectId

from config import CONFIG

def GET(self,dbCollection,search):
    lst = []
    for item in dbCollection.find():
        lst.append({
            "id": str(item.get('_id')),
            "name": item.get("name"),
            "image": f"{CONFIG.getWEB_PROTOCOL()}://{CONFIG.getWEB_HOST()}:{CONFIG.getWEB_PORT()}/image?id="+str(item.get('_id')),
            "number_of_rooms": 1337,
            "qm": 42,
            "floors": 69,
            "vendor": "self",
            "background": "city",
            "facts": "lelele rofl keepo",
        })
    return {"success":True,"list":lst}
