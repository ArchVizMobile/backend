from bson import ObjectId

def POST(self,dbCollection,search):
    if "id" not in search:
        return {"success":False}

    search = {"_id":ObjectId(search["id"])}
    cnt = dbCollection.count_documents(search)
    ret = {
        "success": False,
        "data": self.json
    }

    if cnt > 0:
        self.json["_id"] = search["_id"]
        dbCollection.delete_one(search)
        dbCollection.insert_one(self.json)
        ret["success"] = True

    return ret