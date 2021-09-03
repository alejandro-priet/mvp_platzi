from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

categories = db.Table('categories',
                      db.Column('category_id', db.Integer, db.ForeignKey('category.categoryID'), primary_key=True),
                      db.Column('person_id', db.Integer, db.ForeignKey('person.personID'), primary_key=True)
                      )


class Person(db.Model):
    __tablename__ = 'person'

    personID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.Text(), unique=True)
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
                                 backref=db.backref('users', lazy='dynamic'))
    password_hash = db.Column(db.Text())

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.username, self.password_hash, self.personID, self.categories)


class Category(db.Model):
    __tablename__ = 'category'

    categoryID = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(200), unique=True)

    def __init__(self, categoryname):
        self.categoryname = categoryname

    def __repr__(self):
        return '{}, {}'.format(self.categoryname, self.categoryID)
