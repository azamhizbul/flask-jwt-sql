from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from config import connection

conn = connection.connectMSSQL()

class Products(Resource):
    @jwt_required()
    def get(self):
        data = []
        cur = conn.cursor()
        # working with stored procedure
        query = "exec stp_getAllProduk"
        result = cur.execute(query)
        rows = result.fetchall()
        for i in rows:
            data.append({"id" : i[0], "namaBarang": i[1], "harga": i[2], "stock": i[3]}) 
        return {"data" : data }, 200

    @jwt_required()
    def post(self):
        message = None
        status = None
        try:
            data = request.get_json()
            cur = conn.cursor()
            # working with stored procedure
            query = "exec stp_insertProduct ?,?,?"
            cur.execute(query, (data['namaBarang'], data['hargaBarang'], data['stock']))
            conn.commit()
            message = "data berhasil ditambahkan"
            status = 200
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal ditambahkan"
            status = 400   
        return {"message" : message}, status  

    @jwt_required()
    def put(self):
        message = None
        status = None
        try:
            data = request.get_json()
            cur = conn.cursor()
            print(data)
            # working with stored procedure
            query = "exec stp_editProduk ?,?,?,?"
            cur.execute(query, (data['id'], data['namaBarang'],data['hargaBarang'], data['stock']))
            conn.commit()
            status = 200
            message = "data berhasil diubah"
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal diubah"
            status = 400   
        return {"message" : message}, status   

    @jwt_required()
    def delete(self):
        message = None
        status = None
        try:
            data = request.get_json()
            cur = conn.cursor()
            print(data)
            # working with stored procedure
            query = "exec stp_deleteProduk ?"
            cur.execute(query, (data['id']))
            conn.commit()
            status = 200
            message = "data berhasil dihapus"
        except Exception as e :
            print(e)
            conn.rollback()
            message = "data gagal dihapus"
            status = 400   
        return {"message" : message}, status             

class Product(Resource):
    @jwt_required()
    def get(self,id):
        data = []
        cur = conn.cursor()
        query = "exec stp_getProdukbyID ?"
        result = cur.execute(query, id)
        rows = result.fetchall()
        for i in rows:
            data.append({"id" : i[0], "namaBarang": i[1], "harga": i[2], "stock": i[3]}) 
        return {"data" : data }, 200        
