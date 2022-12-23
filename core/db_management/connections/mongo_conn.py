from pymongo import MongoClient
from django.conf import settings


mongo_client = MongoClient(host=settings.MONGO_HOST,
                           port=int(settings.MONGO_PORT),
                           username=settings.MONGO_INITDB_USERNAME,
                           password=settings.MONGO_INITDB_PASSWORD)

db_handle = mongo_client[settings.MONGO_INITDB_DATABASE]


def get_collection_handle(collection_name):
    return db_handle[collection_name]
