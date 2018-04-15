#haroku database url has been added as an environment variable. an environment variable is something that the system (haroku)
# keeps track of. so that computer is always going to know the value of the environment variable. all we have to to do is to read
# that variable from the environment
import os # give us access to operating system's environment variables
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#use sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # it doesn't have to be sqlite, could be mysql, oracle
#use haroku posgres. what this is gonna do is go to the operating system to ask for its environment variable. if we are in Heroku
#then it is going to read that environment variable and connect to the Posgres app and use that value as the apps Config file
# however we still want to run the app locally for testing purpose, so we also use sqlite locally if the DATABASE_URL is not defined
# so we set sqlite link as default parameter of get(), is DATABASE_URL is not found, we use sqlite instaed
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'EiEiO'
api = Api(app)



jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
