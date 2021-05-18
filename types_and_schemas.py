from mypy_extensions import TypedDict


PostInDB = TypedDict(
    "PostInDB",
    {
        "_id":      int,
        "content":  str,
        "views":    int,
    }
)

PostWithViews = TypedDict(
    "PostWithViews",
    {
        "content":  str,
        "views":    int,
    }
)

post_in_db_schema = {
    "_id":      {"type": "integer", "required": True},
    "content":  {"type": "string",  "required": True},
    "views":    {"type": "integer", "required": True},
}


PostContent = str



