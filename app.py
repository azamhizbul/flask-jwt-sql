from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from account import Account

app = Flask(__name__)
app.secret_key = '123qweasd'
api = Api(app)

jwt = JWT(app, authenticate, identity)


items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=int,
        required=True,
        help="price tidak boleh kosong atau harus angka"
    )
    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404
        # for item in items:
        #     if item['name'] == name :
        #         return item
        # return {"item": None}, 404

    def post(self, name):
        param = next(filter(lambda x: x['name'] == name, items), None)
        if param :
            return {'message': 'item dengan nama {} sudah ada'.format(name)}, 400
        data = request.get_json()
        item = {"name": data['name'], "price":data['price']}
        items.append(item)
        return items, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'data dihapus'}

    def put(self, name) :
        
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {"name": name, "price":data['price']}
            items.append(item)
        else :
            item.update(data)    

        return item        


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'data': items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Account, '/accounts')

app.run(port=5000, debug=True)

