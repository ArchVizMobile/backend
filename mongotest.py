import pymongo

myclient = pymongo.MongoClient("mongodb://api.lisha-app.com:27017/")

mydb = myclient["archviz"]

collist = mydb.list_collection_names()
print(collist)
if "customers" not in collist:
    mycollection = mydb["floorplans"]