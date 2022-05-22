from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from account import Account

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = '123qweasd'
api = Api(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)




api.add_resource(Account, '/accounts')

app.run(port=5000, debug=True)

