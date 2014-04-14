from functools import wraps
from flask import request, Response, jsonify, json
import hashtbl

def check_auth(username, password):
    if hashtbl.verify_password(username, password):
        return True
    return False

def authenticate():
    response =jsonify(dict())
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return response

def login_required(f):
    """Decorator fn that authenticates user/admin """
    @wraps(f) #this fn allows the doc strings of dec fn to be displayed
    def auth_decorator(*args, **kwargs):
        #auth = request.authorization
        username = request.json['username']
        password = request.json['password']
        #if not auth or not check_auth(username, password):
        if not check_auth(username, password):
            return authenticate()
        return f(*args, **kwargs)

    return auth_decorator


