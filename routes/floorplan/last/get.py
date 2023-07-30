import pymongo


def GET(self,dbCollection,search):
    ret = {
        "success": False,
        "walls": [],
        "junctions": [],
        "rooms": [],
        "scale": -1,
    }
    try:
        ret = dbCollection.find_one(
            sort=[( '_id', pymongo.DESCENDING )]
        )
        ret["_id"] = str(ret["_id"])
    except:
        pass
    return ret
