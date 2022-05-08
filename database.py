import pymongo

class DB(object):

    URI = "mongodb://localhost:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['event_cafe_cloud']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def delete(collection, data):
        return DB.DATABASE[collection].delete_one(data)


    @staticmethod
    def find_one(collection, query):
        return DB.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one(collection, query, update):
        return DB.DATABASE[collection].update_one(query, update)

    @staticmethod
    def list(collection, query1, query2):
        return list(DB.DATABASE[collection].find(query1, query2))

    @staticmethod
    def count_documents(collection, query1, query2):
        return DB.DATABASE[collection].find(query1, query2)



