from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    @staticmethod
    @jwt_required()
    def get(name: str) -> (dict, int):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json(), 200
        return {'message': f"Store '{name}' not found"}, 404

    @staticmethod
    @jwt_required()
    def post(name: str) -> (dict, int):
        if StoreModel.find_by_name(name):
            return {'message': f"An store with name '{name}' already exists"}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the store'}, 500

        return store.json(), 201

    @staticmethod
    @jwt_required()
    def delete(name: str) -> (dict, int):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': f"Store '{name}' deleted"}


class StoreList(Resource):
    @staticmethod
    @jwt_required()
    def get() -> (dict, int):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200
