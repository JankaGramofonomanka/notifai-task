import os
import datetime

from flask import Flask, make_response, jsonify, request
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import jwt

from decorators import convert, require_token
import database_interaction as db
import constants as c

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello!"



@app.route("/db_test")
def db_test():

    try:
        cluster = MongoClient(c.MONGODB_URI)

        db = cluster["notifai-task-db"]
        col = db["test-collection"]

        col.update_many(
            {"name": "JOOOHN", "surname": "CENAAAAA!!!!!"}, 
            {"$inc": {"score": 5000}}
        )

        return "success"
    
    except Exception:
        return make_response("internal error", 500)



@app.route("/env_test")
@require_token
def env_test():
    return os.environ["EXAMPLE_ENV_VAR"]



@app.route("/login")
def login():
    try:
        data = request.json
        password = data["password"]
    
    except KeyError:
        return jsonify(c.NO_PASSWORD_MSG), 401
    
    except TypeError:
        return jsonify(c.NO_PASSWORD_MSG), 401


    if password == c.PASSWORD:
        data = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }
        token = jwt.encode(data, c.SECRET_KEY)

        return jsonify({"token": token.decode("UTF-8")})
    
    else:
        return (
            jsonify("Could not verify"), 
            401, 
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )



@app.route("/<post_id>/view", methods=['GET'])
@convert(post_id=int)
def view(post_id : int):
    
    try:
        post = db.get_post(post_id)
        db.increment_views(post_id)

        return jsonify(post)
    
    except db.DataDoesNotExist:
        return jsonify(c.POST_NOT_FOUD_MSG), 404
    
    except db.DatabaseFormatError:
        return jsonify(c.DATABASE_FORMAT_ERROR_MSG), 500



@app.route("/<post_id>/create", methods=['POST'])
@convert(post_id=int)
def create(post_id : int):

    try:
        content = request.json      # type: str
        if type(content) == str and len(content) > 0:
            db.create_post(post_id, content)
            return jsonify(c.POST_CREATED_MSG), 201

        else:
            return jsonify(c.INVALID_CONTENT_MSG), 400

    except DuplicateKeyError:
        return jsonify(c.POST_ALREDY_EXISTS_MSG), 400



@app.route("/<post_id>/edit", methods=['PUT'])
@convert(post_id=int)
def edit(post_id : int):
    
    try:
        content = request.json      # type: str
        if type(content) == str and len(content) > 0:

            db.update_post(post_id, content)
            return jsonify(c.POST_UPDATED_MSG), 200

        else:
            return jsonify(c.INVALID_CONTENT_MSG), 400

    except db.DataDoesNotExist:
        return jsonify(c.POST_NOT_FOUD_MSG), 404



@app.route("/<post_id>/delete", methods=['DELETE'])
@convert(post_id=int)
def delete(post_id : int):

    try:
        db.delete_post(post_id)
        return jsonify(c.POST_DELETED_MSG), 200
    
    except db.DataDoesNotExist:
        return jsonify(c.POST_NOT_FOUD_MSG), 404


if __name__ == "__main__":
    app.run(debug=True)





