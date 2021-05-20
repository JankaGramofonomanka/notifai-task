import os

MONGODB_URI             = os.environ["MONGODB_URI"]
SECRET_KEY              = os.environ["SECRET_KEY"]
PASSWORD                = os.environ["PASSWORD"]
DATABASE_NAME           = os.environ["DATABASE_NAME"]
POST_COLLECTION_NAME    = os.environ["POST_COLLECTION_NAME"]

TOKEN_EXP_TIME = int(os.environ["TOKEN_EXP_TIME"])

MAX_POST_LENGTH = 160

DATABASE_FORMAT_ERROR_MSG   = "Data is corrupt."
INVALID_CONTENT_MSG         = "Request does not contain a valid post."
POST_ALREDY_EXISTS_MSG      = "Post alredy exists."
POST_NOT_FOUD_MSG           = "Post does not exist."
NO_PASSWORD_MSG             = "No password provided."
INVALID_ID_MSG              = "The Id of the post is invalid."

POST_CREATED_MSG = "The post has been created"
POST_UPDATED_MSG = "The post has been updated"
POST_DELETED_MSG = "The post has been deleted"

