from bson import ObjectId

from config import CONFIG

def GET(self,dbCollection,search):
    lst = []
    for item in dbCollection.find():
        lst.append({
            "id": str(item.get('_id')),
            "name": item.get("name"),
            "image": f"{CONFIG.getWEB_PROTOCOL()}://{CONFIG.getWEB_HOST()}:{CONFIG.getWEB_PORT()}/image?id="+str(item.get('_id'))
        })
    return {"success":True,"list":lst}