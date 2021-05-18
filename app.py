import os

from flask import Flask, make_response, jsonify, request
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient

from decorators import convert
import database_interaction as db

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello!"



@app.route("/db_test")
def db_test():

    try:
        cluster = MongoClient(os.environ["MONGODB_URI"])

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
def env_test():
    return os.environ["EXAMPLE_ENV_VAR"]



@app.route("/<post_id>/view", methods=['GET'])
@convert(post_id=int)
def view(post_id : int):
    
    try:
        post = db.get_post(post_id)
        db.increment_views(post_id)

        return jsonify(post)
    
    except db.DataDoesNotExist:
        return jsonify("Post does not exist."), 404
    
    except db.DatabaseFormatError:
        return jsonify("Data is corrupt."), 500



@app.route("/<post_id>/create", methods=['POST'])
@convert(post_id=int)
def create(post_id : int):

    try:
        content = request.json      # type: str
        if type(content) == str and len(content) > 0:
            db.create_post(post_id, content)
            return jsonify("The post has been created"), 201

        else:
            return jsonify("Request does not contain a valid post."), 400

    except DuplicateKeyError:
        return jsonify("Post alredy exists."), 400



@app.route("/<post_id>/edit", methods=['PUT'])
@convert(post_id=int)
def edit(post_id : int):
    
    try:
        content = request.json      # type: str
        if type(content) == str and len(content) > 0:
            
            db.update_post(post_id, content)
            return jsonify("The post has been updated"), 200

        else:
            return jsonify("Request does not contain a valid post."), 400

    except db.DataDoesNotExist:
        return jsonify("Post does not exist."), 404



@app.route("/<post_id>/delete", methods=['DELETE'])
@convert(post_id=int)
def delete(post_id : int):

    try:
        db.delete_post(post_id)
        return jsonify("The post has been deleted"), 200
    
    except db.DataDoesNotExist:
        return jsonify("Post does not exist."), 404


if __name__ == "__main__":
    app.run(debug=True)





