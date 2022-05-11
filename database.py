import pymongo


class DB(object):
    URI = "mongodb://localhost:27017"

    def __init__(self):
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['event_cafe_cloud']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def delete(collection, data):
        return DB.DATABASE[collection].delete_one(data)

    @staticmethod
    def find_one(collection, included_query, excluded_query):
        return DB.DATABASE[collection].find_one(included_query, excluded_query)

    @staticmethod
    def update_one(collection, find_query, update_query):
        return DB.DATABASE[collection].update_one(find_query, update_query)

    @staticmethod
    def list(collection, included_query, excluded_query):
        return list(DB.DATABASE[collection].find(included_query, excluded_query))

    @staticmethod
    def count_documents(collection, query):
        return DB.DATABASE[collection].count_documents(query)

    @staticmethod
    def count_collection(collection):
        return DB.DATABASE[collection].estimated_document_count({})

    @staticmethod
    def allocate_pk(collection, pk):
        try:
            return DB.DATABASE[collection].find_one(sort=[(pk, -1)])[pk] + 1
        except TypeError:
            return 1
