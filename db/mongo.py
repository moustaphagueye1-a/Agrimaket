import os
from pymongo import MongoClient

_client = None

DB_NAME = "terroir_sn"

def get_db():
    global _client

    uri = os.environ.get("MONGO_URI")

    if not uri:
        raise Exception("MONGO_URI non défini")

    if _client is None:
        _client = MongoClient(uri)

    return _client[DB_NAME]


def get_produits():
    return get_db()["produits"]


def get_commandes():
    return get_db()["commandes"]