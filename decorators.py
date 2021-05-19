from functools import wraps

from flask import make_response, request, jsonify
from cerberus import Validator
from cerberus.validator import DocumentError
import jwt

import constants as c
import lib





def convert(**kwtypes : type):
    """
    Returns a decortor that converts string key word arguments of a function 
    to given types (for example, if `kwtypes[param] == int`, then the 
    parameter `param` will be converted to `int`.)

    If it is impossible, the decorated function will return a 400 response.
    """
    
    def decorator(func):
        
        @wraps(func)
        def decorated(**kwargs : str):
            
            for arg, type_of_arg in kwtypes.items():

                try:
                    kwargs[arg] = type_of_arg(kwargs[arg])

                except ValueError:
                    return make_response(
                        f"parameter {arg} should be of type {type}",
                        400
                    )

            return func(**kwargs)
        
        return decorated
    
    return decorator


def require_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        
        if not token:
            return jsonify({"message": "Token is missing."}), 401
        
        try:
            data = jwt.decode(token, c.SECRET_KEY)
        except:
            return jsonify(lib.json_msg("Token is invalid.")), 401

        return func(*args, **kwargs)

    return decorated




def assert_json(schema, error_msg, error_code):

    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            validator = Validator(schema)

            data = request.json

            try:
                if validator.validate(data):
                    return func(*args, **kwargs)
                    
                else:
                    return jsonify(lib.json_msg(error_msg)), error_code

            except DocumentError:
                return jsonify(lib.json_msg(error_msg)), error_code
                
    
        return decorated

    return decorator




