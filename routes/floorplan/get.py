from bson import ObjectId

def GET(self,dbCollection,search):
    if "id" not in search:
        return {"success":False}

    search = {"_id":ObjectId(search["id"])}
    cnt = dbCollection.count_documents(search)
    ret = {
        "success": False,
        "walls": [],
        "junctions": [],
        "rooms": [],
        "scale": -1,
    }

    if cnt > 0:
        lst = dbCollection.find(search)
        ret = lst[0]
        ret["_id"] = str(ret["_id"])

    return ret