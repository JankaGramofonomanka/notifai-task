import datetime

from flask import Flask, make_response, jsonify, request
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import jwt

from decorators import require_token, assert_json, assert_id
import lib
import constants as c
from types_and_schemas import json_passwd_schema
from types_and_schemas import post_content_schema

app = Flask(__name__)




@app.route("/")
def hello():
    return "Hello!"



# -----------------------------------------------------------------------------
@app.route("/login", methods=["POST"])
@assert_json(json_passwd_schema, c.NO_PASSWORD_MSG, 401)
def login():
    
    password = request.json["password"]
    
    if password == c.PASSWORD:
        
        now = datetime.datetime.utcnow()
        exp_time = datetime.timedelta(minutes=c.TOKEN_VALIDITY_TIME)
        exp_date = now + exp_time
        token = jwt.encode({"exp": exp_date}, c.SECRET_KEY)

        return jsonify({"token": token.decode("UTF-8")})
    
    else:
        return lib.jsonify_msg("Could not verify"), 401



# -----------------------------------------------------------------------------
@app.route("/<post_id>", methods=["GET"])
@assert_id
def view(post_id : ObjectId):
    
    try:
        post = lib.get_post(post_id)
        lib.increment_views(post_id)

        return jsonify(post)
    
    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404
    
    except lib.DatabaseFormatError:
        return lib.jsonify_msg(c.DATABASE_FORMAT_ERROR_MSG), 500



# -----------------------------------------------------------------------------
@app.route("/create", methods=["POST"])
@require_token
@assert_json(post_content_schema, c.INVALID_CONTENT_MSG, 400)
def create():

    try:
        content = request.json["content"]   # type: str
        post_id = lib.create_post(content)
        return jsonify({"id": str(post_id)}), 201

    except DuplicateKeyError:
        return lib.jsonify_msg(c.POST_ALREDY_EXISTS_MSG), 400



# -----------------------------------------------------------------------------
@app.route("/<post_id>", methods=["PUT"])
@require_token
@assert_id
@assert_json(post_content_schema, c.INVALID_CONTENT_MSG, 400)
def edit(post_id : ObjectId):
    
    try:
        content = request.json["content"]   # type: str
        lib.update_post(post_id, content)
        return lib.jsonify_msg(c.POST_UPDATED_MSG), 200

    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404



# -----------------------------------------------------------------------------
@app.route("/<post_id>", methods=["DELETE"])
@require_token
@assert_id
def delete(post_id : ObjectId):

    try:
        lib.delete_post(post_id)
        return lib.jsonify_msg(c.POST_DELETED_MSG), 200
    
    except lib.DataDoesNotExist:
        return lib.jsonify_msg(c.POST_NOT_FOUD_MSG), 404



# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)





