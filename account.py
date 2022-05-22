from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from sqlite3 import Error
from security import authenticate, identity
from connectionDB import connect

conn = connect()

def callLast():
    with connect():
        cur = connect().cursor()
        query = "select * from user order by id DESC limit 1"
        result = cur.execute(query)
        row = result.fetchone()
        return row
        

class Account(Resource):
    # @jwt_required()
    def get(self):
        data = []
        with connect():
            cur = connect().cursor()
            query = "select * from user"
            result = cur.execute(query)
            rows = result.fetchall()
            for i in rows:
                data.append({"id" : i[0], "username": i[1]}) 
                
            
            return {"data" : data }, 200

    @jwt_required()
    def post(self):
        message = None
        conn = connect()
        try:
            currentId = callLast()[0]
            data = request.get_json()
            cur = conn.cursor()
            query = "INSERT INTO 'user' (id,username,password) VALUES (?,?,?)"
            cur.execute(query, (currentId+1, data['username'], data['password']))
            conn.commit()
            message = "data berhasil ditambahkan"
        except Error as e :
            print(e)
            conn.rollback()
            message = "data gagal ditambahkan"
        finally :
            conn.close()    
        return {"message" : message}

    @jwt_required()
    def put(self):
        message = None
        conn = connect()
        try:
            data = request.get_json()
            cur = conn.cursor()
            query = "update user set username=?, password=? where id=?"
            cur.execute(query, (data['username'],data['password'],data['id']))
            conn.commit()
            message = "data berhasil diubah"
        except Error as e :
            print(e)
            conn.rollback()
            message = "data gagal diubah"
        finally :
            conn.close()    
        return {"message" : message}    

    @jwt_required()
    def delete(self):
        message = None
        conn = connect()
        try:
            data = request.get_json()
            cur = conn.cursor()
            query = "delete from user where rowid=?"
            cur.execute(query, (data['id'],))
            conn.commit()
            message = "data berhasil dihapus"
        except Error as e :
            print(e)
            conn.rollback()
            message = "data gagal dihapus"
        finally :
            conn.close()    
        return {"message" : message} 
