from flask import jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from cerberus import Validator

from types_and_schemas import PostInDB
from types_and_schemas import PostWithViews
from types_and_schemas import post_in_db_schema
from types_and_schemas import JSONMessage

from exceptions import DatabaseFormatError
from exceptions import DataDoesNotExist

import constants as c


def json_msg(msg : str) -> JSONMessage:
    return {"message": msg}

def jsonify_msg(msg : str):
    return jsonify(json_msg(msg))

def get_collection():
    cluster = MongoClient(c.MONGODB_URI)

    return cluster[c.DATABASE_NAME][c.POST_COLLECTION_NAME]



def get_post(post_id : ObjectId) -> PostWithViews:

    collection = get_collection()
    post = collection.find_one({"_id": post_id})    # type: PostInDB

    if post is None:
        raise DataDoesNotExist


    validator = Validator(post_in_db_schema)
    if validator.validate(post):

        result = {
            "content":  post["content"],
            "views":    post["views"],
        }                                           # type: PostWithViews
        return result
    
    else:            
        raise DatabaseFormatError



def increment_views(post_id : ObjectId) -> None:

    collection = get_collection()
    result = collection.update_one({"_id": post_id}, {"$inc": {"views": 1}})

    if result.modified_count == 0:
        raise DataDoesNotExist



def create_post(content : str) -> ObjectId:
    collection = get_collection()
    result = collection.insert_one({"content": content, "views": 0})
    post_id = result.inserted_id    # type: ObjectId

    return post_id



def update_post(post_id : ObjectId, content : str) -> None:

    collection = get_collection()
    result = collection.update_one(
        {"_id": post_id}, 
        {"$set": {"content": content, "views": 0}}
    )

    if result.modified_count == 0:
        raise DataDoesNotExist



def delete_post(post_id : ObjectId) -> None:
    collection = get_collection()
    result = collection.delete_one({"_id": post_id})
    
    if result.deleted_count == 0:
        raise DataDoesNotExist









