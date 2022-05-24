from datetime import timedelta
from flask import Flask
from flask_restful import Api
from account import Account
from userAuth import UserAuth
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = '123qweasd'
api = Api(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)

api.add_resource(Account, '/accounts')
api.add_resource(UserAuth, '/login')

if __name__ == "__main__":
    app.run()

app.run(port=5000, debug=True)