from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from item import Item, ItemList
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDA2MzY2ODksImlhdCI6MTYwMDYzNjM4OSwibmJmIjoxNjAwNjM2Mzg5LCJpZGVudGl0eSI6MX0.9J6vJLiGFhLSjLzWna0o6kTsFa5NAe6cqTy2WL4TcH8'


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run()
