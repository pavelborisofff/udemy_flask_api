import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )

    @staticmethod
    def post() -> (dict, int):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': f"An user with name '{data['username']}' already exists"}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        # cursor.execute(query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        user = UserModel(**data)
        user.save_to_db()

        return {'message':  f"User '{data['username']}' created successfully"}, 201
