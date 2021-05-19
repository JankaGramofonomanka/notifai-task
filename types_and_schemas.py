from mypy_extensions import TypedDict
from bson.objectid import ObjectId

import constants as c

PostInDB = TypedDict(
    "PostInDB",
    {
        "_id"       : ObjectId,
        "content"   : str,
        "views"     : int,
    }
)

PostWithViews = TypedDict(
    "PostWithViews",
    {
        "content"   : str,
        "views"     : int,
    }
)

post_in_db_schema = {
    "_id":      {"required": True},
    "content":  {"required": True, "type": "string"},
    "views":    {"required": True, "type": "integer"},
}




JSONMessage     = TypedDict("JSONMessage",  {"message"  : str})

json_msg_schema     = {"message":   {"type": "string", "required": True}}
json_passwd_schema  = {"password":  {"type": "string", "required": True}}
post_content_schema = {
    "content": {
        "type": "string", 
        "required": True,
        "maxlength": c.MAX_POST_LENGTH,
        "minlength": 1,
    }
}





