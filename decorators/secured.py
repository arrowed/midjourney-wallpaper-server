# thanks armin http://flask.pocoo.org/snippets/70/

import time
from functools import update_wrapper
from uuid import uuid4
from flask import request, g

class Secured(object):
    expiration_window = 10

    def __init__(self): #, key_prefix, limit, per, send_x_headers, redis):
        pass

def on_over_limit():
    return 'Unauthorised', 403

def get_token():
    arg = request.args.get('Authorization')
    hea = request.headers.get('Authorization')
    
    print ('args ', arg)
    print('headers: ', hea)
    
    return arg or hea

def reset_token(app):
    import uuid
    t = uuid4().hex
    app.config['red'].set('token', t)
    print('Reset auth token to ', t)

def secured(app, per=300, invalid_token=on_over_limit):
    def decorator(f):
        def secure_check(*args, **kwargs):
            token = get_token()

            tokens = app.config['allowed_keys']
            print('Got token from user ', token, ', wanted ', tokens)

            if not token in tokens:
                return invalid_token()
            return f(*args, **kwargs)
        return update_wrapper(secure_check, f)
    return decorator