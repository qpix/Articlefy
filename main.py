import a
import authorize
import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='http://127.0.0.1:3000', supports_credentials=True)

def info(message):
    return json.dumps({
        'info': message
    })

def error(message, code=400):
    return json.dumps({
        'error': str(message)
    }), code

@app.route('/', methods=['GET'])
@authorize.basic
def get_articles():
    return json.dumps(a.list_articles(authorize.get_username()))

@app.route('/<title>', methods=['POST'])
@authorize.basic
def create_article(title):
    try:
        a.create_article(authorize.get_username(), title, request.data.decode('utf-8'))
        return info('Article created successfully.')
    except Exception as e:
        return error(e)

@app.route('/<title>', methods=['GET'])
@authorize.basic
def get_article(title):
    try:
        return a.get_article(authorize.get_username(), title)
    except FileNotFoundError:
        return error('Article not found.', 404)
    except Exception as e:
        return error(e)

@app.route('/<title>', methods=['DELETE'])
@authorize.basic
def delete_article(title):
    try:
        a.delete_article(authorize.get_username(), title)
        return info('Article deleted successfully.')
    except FileNotFoundError:
        return error('Article not found.', 404)
    except Exception as e:
        return error(e)
