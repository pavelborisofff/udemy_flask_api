import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='THis field cannot be left blank'
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name, ))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        # return next((item for item in items if item['name'] == name), None)
        # Можно так: next(filter(lambda x: x['name'] == name, items), None)

    @staticmethod
    @jwt_required()
    def get(name):
        item = Item.find_by_name(name)

        if item:
            return item, 200
        return {'message': f"Item '{name}' not found"}, 404

        # return {'item': item}, 200 if item else 404

    @staticmethod
    def post(name):
        if Item.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400

        # data = request.get_json()  # force=True без проверки заголовков типа данных, silent=True не вернёт ошибку
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # Internal server error

        return item, 201

    @staticmethod
    def insert(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (NULL, ?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @staticmethod
    def update(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @staticmethod
    @jwt_required()
    def delete(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        # items = [item for item in items if item['name'] != name]  # list(filter(lambda x: x['name'] != name, items))
        return {'message': f"Item '{name}' deleted"}

    @staticmethod
    @jwt_required()
    def put(name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if not item:
            try:
                Item.insert(updated_item)
                return updated_item, 201
            except:
                return {'message': 'An error occurred insert the item'}, 500
        else:
            try:
                Item.update(updated_item)
                return updated_item, 201
            except:
                return {'message': 'An error occurred update the item'}, 500


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = [{'name': row[1], 'price': row[2]}for row in cursor.execute(query)]

        connection.commit()
        connection.close()

        return {'items': result}