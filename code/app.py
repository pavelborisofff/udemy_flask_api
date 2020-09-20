from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []

'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDA2MzY2ODksImlhdCI6MTYwMDYzNjM4OSwibmJmIjoxNjAwNjM2Mzg5LCJpZGVudGl0eSI6MX0.9J6vJLiGFhLSjLzWna0o6kTsFa5NAe6cqTy2WL4TcH8'

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='THis field cannot be left blank'
    )

    @staticmethod
    def item_exists(name):
        return next((item for item in items if item['name'] == name), None)
        # Можно так: next(filter(lambda x: x['name'] == name, items), None)

    @staticmethod
    # @jwt_required()
    def get(name):
        item = Item.item_exists(name)

        return {'item': item}, 200 if item else 404

    @staticmethod
    # @jwt_required()
    def post(name):
        if Item.item_exists(name):
            return {'message': f"An item with name '{name}' already exists"}, 400

        # data = request.get_json()  # force=True без проверки заголовков типа данных, silent=True не вернёт ошибку
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @staticmethod
    # @jwt_required()
    def delete(name):
        global items
        items = [item for item in items if item['name'] != name]  # list(filter(lambda x: x['name'] != name, items))
        return {'message': f"Item '{name}' deleted"}

    @staticmethod
    # @jwt_required()
    def put(name):
        data = Item.parser.parse_args()
        item = Item.item_exists(name)
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run()
