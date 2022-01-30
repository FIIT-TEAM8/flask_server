import os
from bson.json_util import loads, dumps
from pymongo import MongoClient
import api.v2.api_settings as api_settings

class Database(object):
    DATABASE = None

    # static method, no need to create database object
    @staticmethod
    def initialize():
        # mongo db configuration
        # connection = MongoClient('localhost', 27017)
        
        connection = MongoClient(
            host='mongo_db:27017',
            serverSelectionTimeoutMS = 3000,
            username=api_settings.MONGO_INITDB_ROOT_USERNAME,
            password=api_settings.MONGO_INITDB_ROOT_PASSWORD
        )

        # connect to admin DB in Mongo
        Database.DATABASE = connection['admin']
        # Database.DATABASE = connection['amsdb']

        # connect to 'articles' collection
        articles_collection = Database.DATABASE['articles']

        # connect to 'crimemaps' collection
        crimemaps_collection = Database.DATABASE['crimemaps']

    
    @staticmethod
    def find(collection, to_select):
        return Database.DATABASE[collection].find(to_select)


    @staticmethod
    def find_one(collection, to_select, fields_to_select=False):
        if fields_to_select:
            return Database.DATABASE[collection].find_one(to_select, fields_to_select)
        else:
            return Database.DATABASE[collection].find_one(to_select)