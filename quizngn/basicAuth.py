from functools import wraps
from flask import request, Response, jsonify, json
import hashtbl

def check_auth(username, password):
    if hashtbl.ht.verify_password(username, password):
        return True
    return False

def authenticate():
    response =jsonify(dict())
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    response.location = '/admnusers'
    return response

def login_required(f):
    """Decorator fn that authenticates user/admin """
    @wraps(f) #this fn allows the doc strings of dec fn to be displayed
    def auth_decorator(*args, **kwargs):
        '''
        username = request.json['username']
        password = request.json['password']
        '''
        # get username password from HTTP Basic Authentication header in 
        # request- Authorization: 'Basic username:password'
        print "\n-------basicauth.py; login required------\n"
        auth = request.headers.get('Authorization')
        if not auth:
            return authenticate()
        username, password = tuple((auth.rsplit().pop()).rsplit(':'))
        if not check_auth(username, password):
            #Maybe we need to set a flag to limit the no of times
            # we shoudl authenticate?
            return authenticate()
        return f(*args, **kwargs)

    return auth_decorator


