import pymongo
from config import Auth

mongo = pymongo.MongoClient("mongodb+srv://admin0001:llWW6Pw4FjmRtzNA@bot.ggs2v.mongodb.net/main?retryWrites=true&w=majority")
db = mongo.cp_new

def set(collection, id, data):
    i = {"_id":id}
    if db[collection].count_documents({"_id":id}) == 0:
        db[collection].insert_one({**i, **data})
    else:
        db[collection].update_one(i, {"$set":data})