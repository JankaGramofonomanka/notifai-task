from flask import make_response





def convert(**kwtypes : type):
    """
    Returns a decortor that converts string key word arguments of a function 
    to given types (for example, if `kwtypes[param] == int`, then the 
    parameter `param` will be converted to `int`.)

    If it is impossible, the decorated function will return a 400 response.
    """
    
    def decorator(func):
        
        def real_func(**kwargs : str):
            
            for arg, type_of_arg in kwtypes.items():

                try:
                    kwargs[arg] = type_of_arg(kwargs[arg])

                except ValueError:
                    return make_response(
                        f"parameter {arg} should be of type {type}",
                        400
                    )

            return func(**kwargs)
        
        return real_func
    
    return decorator



