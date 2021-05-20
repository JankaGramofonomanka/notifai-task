from functools import wraps
from typing import Dict, Any
from string import hexdigits

from flask import make_response, request
from cerberus import Validator
from cerberus.validator import DocumentError
import jwt
from bson.objectid import ObjectId
from bson.errors import InvalidId

import constants as c
import lib




# -----------------------------------------------------------------------------
def require_token(func):
    """
    Checks if a valid acces token is provided, 
    if not, returns an 'Unauthorized' response.
    """

    @wraps(func)
    def decorated(*args, **kwargs):

        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        
        if not token:
            return lib.jsonify_msg("Token is missing."), 401
        
        try:
            data = jwt.decode(token, c.SECRET_KEY)

        except:
            return lib.jsonify_msg("Token is invalid."), 401

        return func(*args, **kwargs)

    return decorated




# -----------------------------------------------------------------------------
def assert_json(schema : Dict[str, Any], error_msg : str, error_code : int):
    """
    Asserts, that the body of the request is in json format and it has the 
    correct schema
    """

    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            validator = Validator(schema, allow_unknown=True)

            data = request.json

            try:
                if validator.validate(data):
                    return func(*args, **kwargs)
                    
                else:
                    return lib.jsonify_msg(error_msg), error_code

            except DocumentError:
                return lib.jsonify_msg(error_msg), error_code
                
    
        return decorated

    return decorator




# -----------------------------------------------------------------------------
def assert_id(func):
    """
    Converts the keyword argument `post_id` to `ObjectId` and if it is 
    impossible, returns an error message
    """

    @wraps(func)
    def decorated(post_id : str, **kwargs):

        bad_response = lib.jsonify_msg(c.INVALID_ID_MSG), 400

        # check if `post_id` represents a hexadecimal number
        # and has the right length
        if (
            len(post_id) != 24 
            or any(char not in hexdigits for char in post_id)
        ):
            return bad_response
        
        # as far as I know, the above condition is enough to ensure the 
        # validity of `post_id`, but just in case I put this in a try-except 
        # block
        try:
            post_id = ObjectId(post_id)
        
        except InvalidId:
            return bad_response

        except TypeError:
            return bad_response
        
        except ValueError:
            return bad_response
        

        return func(post_id=post_id, **kwargs)
    
    return decorated


