from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Person(db.Model):
    __tablename__ = 'person'

    personID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.Text(), unique=True)
    password_hash = db.Column(db.Text())

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '{}, {}, {}'.format(self.username, self.password_hash, self.personID)


