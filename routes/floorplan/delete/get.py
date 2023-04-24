from bson import ObjectId

def GET(self,dbCollection,search):
    if "id" not in search:
        return {"success":False}

    search = {"_id":ObjectId(search["id"])}
    cnt = dbCollection.count_documents(search)
    ret = {
        "success": False,
    }

    if cnt > 0:
        lst = dbCollection.delete_one(search)
        ret["success"]=True

    return ret