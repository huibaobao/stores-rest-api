from app import app
from db import db

db.init_app(app)

@app.before_first_request  # flask decorator
def create_tables():
    db.create_all() # create all the tables in the file unless it exists already. it come with SQLALCHEMY
