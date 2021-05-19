import os
import datetime

from flask import Flask, make_response, jsonify, request
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import jwt

from decorators import convert, require_token, assert_json
import lib
import constants as c
from types_and_schemas import json_passwd_schema
from types_and_schemas import post_content_schema

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello!"





@app.route("/login")
@assert_json(json_passwd_schema, c.NO_PASSWORD_MSG, 401)
def login():
    
    password = request.json["password"]
    
    if password == c.PASSWORD:
        
        exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({"exp": exp_date}, c.SECRET_KEY)

        return jsonify({"token": token.decode("UTF-8")})
    
    else:
        return lib.jsonify_msg("Could not verify"), 401



@app.route("/<post_id>/view", methods=['GET'])
@convert(post_id=int)
def view(post_id : int):
    
    try:
        post = lib.get_post(post_id)
        lib.increment_views(post_id)

        return jsonify(post)
    
    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404
    
    except lib.DatabaseFormatError:
        return lib.jsonify_msg(c.DATABASE_FORMAT_ERROR_MSG), 500



@app.route("/<post_id>/create", methods=['POST'])
@require_token
@assert_json(post_content_schema, c.INVALID_CONTENT_MSG, 400)
@convert(post_id=int)
def create(post_id : int):

    try:
        content = request.json["content"]   # type: str
        lib.create_post(post_id, content)
        return lib.jsonify_msg(c.POST_CREATED_MSG), 201

    except DuplicateKeyError:
        return lib.jsonify_msg(c.POST_ALREDY_EXISTS_MSG), 400



@app.route("/<post_id>/edit", methods=['PUT'])
@require_token
@assert_json(post_content_schema, c.INVALID_CONTENT_MSG, 400)
@convert(post_id=int)
def edit(post_id : int):
    
    try:
        content = request.json["content"]   # type: str
        lib.update_post(post_id, content)
        return lib.jsonify_msg(c.POST_UPDATED_MSG), 200

    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404



@app.route("/<post_id>/delete", methods=['DELETE'])
@require_token
@convert(post_id=int)
def delete(post_id : int):

    try:
        lib.delete_post(post_id)
        return lib.jsonify_msg(c.POST_DELETED_MSG), 200
    
    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404



if __name__ == "__main__":
    app.run(debug=True)





