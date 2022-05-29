from datetime import timedelta
from flask import Flask
from flask_restful import Api
from modules import user, auth, product
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = '123qweasd'
api = Api(app)


app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)


api.add_resource(user.User, '/user')
api.add_resource(auth.UserAuth, '/login')
api.add_resource(product.Products, '/products')
api.add_resource(product.Product, '/product/<int:id>')

if __name__ == "__main__":
    app.run()

app.run(port=5000, debug=True)