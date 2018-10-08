
import pymongo
class Database(object):
    URI="mongodb://127.0.0.1:27017"
    DATABASE=None

    @staticmethod
    def initialize():
        client=pymongo.MongoClient(Database.URI)
        Database.DATABASE=client['smartCart']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)


    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)


    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query,sort=[( '$natural', -1 )])

    @staticmethod
    def find_one_queue(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection,query1,query2):
        return Database.DATABASE[collection].update(query1,{"$set":query2},multi=True)
