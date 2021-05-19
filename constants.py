import os

MONGODB_URI = os.environ["MONGODB_URI"]
SECRET_KEY = os.environ["SECRET_KEY"]
PASSWORD = os.environ["PASSWORD"]

DATABASE_NAME = "notifai-task-db"
POST_COLLECTION_NAME = "posts"

MAX_POST_LENGTH = 160

DATABASE_FORMAT_ERROR_MSG = "Data is corrupt."
INVALID_CONTENT_MSG = "Request does not contain a valid post."
POST_ALREDY_EXISTS_MSG = "Post alredy exists."
POST_NOT_FOUD_MSG = "Post does not exist."
NO_PASSWORD_MSG = "No password provided."

POST_CREATED_MSG = "The post has been created"
POST_UPDATED_MSG = "The post has been updated"
POST_DELETED_MSG = "The post has been deleted"

