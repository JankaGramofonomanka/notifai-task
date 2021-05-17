import os

from flask import Flask, make_response
import pymongo
from pymongo import MongoClient


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



if __name__ == "__main__":
    app.run()





