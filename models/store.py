from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #back referencen, allow a store to see which items are in items database or in the items table
    items = db.relationship('ItemModel', lazy='dynamic') # list of many items since one store usually have many items
    # lazy='dynamic' tell SQLachemy do not go into the items table and create an object for each item yet

    def __init__(self, name):
        self.name = name

    def json(self):
        # when we use lazy ='dynamic, self.items no longer is a list of items,it is a query builder that has the ablility
        #to look into the items table,then we can use .all to retrieve all of the items in that table
        # which means until we call json() we are not looking into the table, which means that createing stores is very 
        #simple,however, it also means that every time we call json() we have to go into the table , then is will be slower
        # So, there is a trade off between speed of creating the store and speed of calling the json method
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
