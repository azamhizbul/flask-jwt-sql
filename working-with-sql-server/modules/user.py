from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
import bcrypt
from config import connection

conn = connection.connectMSSQL()

def crypto(param):
    param = param.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(param, salt)     
    return hashed   

class User(Resource):
    @jwt_required()
    def get(self):
        data = []
        cur = conn.cursor()
        query = "select * from customers.[user]"
        result = cur.execute(query)
        rows = result.fetchall()
        for i in rows:
            data.append({"id" : i[0], "username": i[1]}) 
        return {"data" : data }, 200

    @jwt_required()
    def post(self):
        message = None
        try:
            data = request.get_json()
            hash = crypto(data['password'])
            cur = conn.cursor()
            query = "INSERT INTO customers.[user](username,password) VALUES (?,?)"
            cur.execute(query, (data['username'], hash))
            conn.commit()
            message = "data berhasil ditambahkan"
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal ditambahkan"   
        return {"message" : message}

    @jwt_required()
    def put(self):
        message = None
        try:
            data = request.get_json()
            cur = conn.cursor()
            query = "update customers.[user] set username=?, where id=?"
            cur.execute(query, (data['username'],data['id']))
            conn.commit()
            message = "data berhasil diubah"
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal diubah"
        return {"message" : message}    

    @jwt_required()
    def delete(self):
        message = None
        try:
            data = request.get_json()
            cur = conn.cursor()
            query = "delete from customers.[user] where id=?"
            cur.execute(query, (data['id'],))
            conn.commit()
            message = "data berhasil dihapus"
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal dihapus"
        return {"message" : message} 
