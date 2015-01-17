from app import db
import json

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    isCritic = db.Column(db.Boolean())
    
    bio = db.Column(db.String(255))
    criticPublication = db.Column(db.String(120))

    session = db.Column(db.String(120))

    def __repr__(self):
        cleaned = {}
        for key in self.__dict__:
            if(key[0] != '_'):
                cleaned[key] = self.__dict__[key]
        return json.dumps(cleaned)

    def to_dict(self):
        cleaned = {}
        for key in self.__dict__:
            if(key[0] != '_'):
                cleaned[key] = self.__dict__[key]
        return cleaned