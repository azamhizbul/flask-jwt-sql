from hmac import compare_digest
from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from connectionDB import connect
import bcrypt

app = Flask(__name__)
conn = connect()

jwt = JWTManager(app)

class UserAuth(Resource):
    def non_empty_string(s):
        if not s:
            raise ValueError
        return s

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=non_empty_string,
        required=True,
        help="username tidak boleh kosong"
    )
    parser.add_argument('password',
        type=non_empty_string,
        required=True,
        help="password tidak boleh kosong"
    )
    
    def post(self): 
        payload = UserAuth.parser.parse_args()
        res = None   
        cur = connect().cursor()
        query = "select * from user where username=?"
        result = cur.execute(query, (payload['username'],))
        row = result.fetchone()

        if row is None :
            res = {"data": "username tidak ada"}, 404
            return res

        compare = bcrypt.checkpw(payload['password'].encode('utf-8'), row[2])

        if compare is False :
            res = {"data": "passwor salah"}, 401
            return res
        data = {
            "id":row[0],
            "username":row[1]
        }    

        access_token = create_access_token(identity=data)
        res = {"access_token":access_token}
        return res

    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        return {"data": user}