# TODO authentication REST api in python
# TODO python REST api for cloud storage
# TODO react/node.js frontend for cloud storage

from flask import Flask
from flask import request
import json
from AuthConnector import AuthConnector
from SQLiteAuthConnector import SQLiteAuthConnector
from PasswordValidator import PasswordValidator
from UsernameValidator import UsernameValidator

app = Flask(__name__)

auth_connector:AuthConnector = SQLiteAuthConnector("auth.db")
password_validator:PasswordValidator = PasswordValidator()
username_validator:UsernameValidator = UsernameValidator()

@app.route('/login')
def login():
    user_name = request.args.get('user')
    password = request.args.get('password')
    if(user_name==None or password==None):
        return '{}', 400
    try:
        hash_entry = auth_connector.get_hash(user_name)
        valid_password = password_validator.validate_password(password, hash_entry)
        if(not valid_password):
            return '{}', 401

        successObject = {
            "user": user_name,
            "token": "TO BE ASSIGNED"
        }

        return json.dumps(successObject), 200
    
    except ValueError as e:
        return '{}', 401
    except:
        return '{}', 500

@app.route('/register')
def register():
    user_name = request.args.get('user')
    password = request.args.get('password')

    if(user_name==None or password==None):
        return '<p>Bad Request</p>', 400
    
    # Validate username
    valid_username = username_validator.validate_username(user_name)
    if(not valid_username):
        return '<p>Invalid username</p>', 400

    # Create a new password hash entry and add to db
    hash_entry = password_validator.generate_password_hash_entry(user_name, password)
    auth_connector.register_user(user_name, hash_entry)
    return f'<p>Successfully registered user {user_name}</p>'