from mypy_extensions import TypedDict

import constants as c

PostInDB = TypedDict(
    "PostInDB",
    {
        "_id"       : int,
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
    "_id":      {"type": "integer", "required": True},
    "content":  {"type": "string",  "required": True},
    "views":    {"type": "integer", "required": True},
}




JSONMessage     = TypedDict("JSONMessage",  {"message"  : str})
JSONPassword    = TypedDict("JSONPassword", {"password" : str})
PostContent     = TypedDict("PostContent",  {"content"  : str})

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





