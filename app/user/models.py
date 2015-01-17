from app import db
import json

class User(db.Model):
    __tablename__ = 'users'
    _hidden = ['session', 'password']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    isCritic = db.Column(db.Boolean())
    
    bio = db.Column(db.String(255))
    criticPublication = db.Column(db.String(120))

    session = db.Column(db.String(120))

    highest_review = db.Column(db.Integer)
    lowest_review = db.Column(db.Integer)
    average_review = db.Column(db.Integer)

    def __repr__(self):
        cleaned = {}
        for key in self.__dict__:
            if(key[0] != '_' and key not in self._hidden):
                cleaned[key] = self.__dict__[key]
        return json.dumps(cleaned)

    def to_dict(self):
        cleaned = {}
        for key in self.__dict__:
            if(key[0] != '_' and key != 'session'):
                cleaned[key] = self.__dict__[key]
        print("Done!", cleaned)
        return cleaned