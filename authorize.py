from flask import request
from functools import wraps
from base64 import b64decode
import csv

def get_basic_authorization_components():
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise Exception('Missing Authorization header.')
    authorization = authorization.split(' ')

    if authorization[0].lower() != 'basic':
        raise Exception('The request does not follow the Basic HTTP Authentication format.')

    try:
        string = b64decode(authorization[1]).decode('UTF-8')
        user_pass = string.split(':')
        return {
            'username': user_pass[0],
            'password': user_pass[1]
        }
    except:
        raise Exception('The requests authorization string is malformed.')

def get_username():
    return get_basic_authorization_components()['username']

def check_username_password(username, password):
    with open('users.csv') as csvfile:
        reader = csv.reader(csvfile)
        for user_pass in reader:
            if user_pass[0] == username and user_pass[1] == password:
                return True
        return False

def basic(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            auth = get_basic_authorization_components()
        except Exception as e:
            return str(e), 400

        authorized = check_username_password(
            auth['username'],
            auth['password']
        )

        if authorized:
            return f(*args, **kwds)
        else:
            return 'The username or password is incorrect.', 401
    return wrapper
