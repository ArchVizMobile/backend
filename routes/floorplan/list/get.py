from bson import ObjectId

def GET(self,dbCollection,search):
    lst = []
    for item in dbCollection.find():
        lst.append({
            "id": str(item.get('_id')),
            "name": item.get("name"),
            "image": "/image/"+str(item.get('_id'))
        })
    return {"success":True,"list":lst}