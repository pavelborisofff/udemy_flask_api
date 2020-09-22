from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='THis field cannot be left blank'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store_id'
    )

    @staticmethod
    @jwt_required()
    def get(name: str) -> (dict, int):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        return {'message': f"Item '{name}' not found"}, 404

        # return {'item': item}, 200 if item else 404

    @staticmethod
    @jwt_required()
    def post(name: str) -> (dict, int):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400

        # data = request.get_json()  # force=True без проверки заголовков типа данных, silent=True не вернёт ошибку
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # Internal server error

        return item.json(), 201

    @staticmethod
    @jwt_required()
    def delete(name: str) -> (dict, int):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': f"Item '{name}' deleted"}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = 'DELETE FROM items WHERE name=?'
        # cursor.execute(query, (name, ))
        #
        # connection.commit()
        # connection.close()

        # items = [item for item in items if item['name'] != name]  # list(filter(lambda x: x['name'] != name, items))

    @staticmethod
    @jwt_required()
    def put(name: str) -> (dict, int):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    @staticmethod
    @jwt_required()
    def get() -> (dict, int):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'SELECT * FROM items'
        # result = [{'name': row[1], 'price': row[2]}for row in cursor.execute(query)]
        #
        # connection.commit()
        # connection.close()
        #
        # return {'items': result}, 200
