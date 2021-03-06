import os

from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, ItemList
from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
# app.config['JWT_AUTH_URL_RULE'] = '/login'

app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run()
