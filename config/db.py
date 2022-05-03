#import mongoClient
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        pass

    def get_db(self):
        url = "mongodb+srv://meotism:Mewtism1@cluster0.iqxih.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        database_name = "myFirstDatabase"
        client = MongoClient(url)
        db = client[database_name]
        return db
