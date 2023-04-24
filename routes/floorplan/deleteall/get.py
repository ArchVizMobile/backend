from bson import ObjectId

def GET(self,dbCollection,search):
    cnt = dbCollection.count_documents({})
    ret = {
        "success": False,
    }

    if cnt > 0:
        found = dbCollection.find({})
        for item in found:
            lst = dbCollection.delete_one(item)
        ret["success"]=True

    return ret