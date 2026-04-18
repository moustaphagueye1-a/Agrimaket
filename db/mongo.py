import os
from pymongo import MongoClient

_client = None

def get_db():
    global _client
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/terroir_sn")
    if _client is None:
        _client = MongoClient(uri)
    db_name = uri.split("/")[-1]
    return _client[db_name]

def get_produits():
    return get_db()["produits"]

def get_commandes():
    return get_db()["commandes"]