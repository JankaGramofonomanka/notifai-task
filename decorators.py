from functools import wraps

from flask import make_response, request, jsonify
import jwt

import constants as c





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

            return func(*args, **kwargs)

        except:
            return jsonify({"message": "Token is invalid."}), 401

    return decorated
