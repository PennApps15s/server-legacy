from app import db
import json

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    reviewId = db.Column(db.Integer)
    
    score = db.Column(db.Integer)
    reviewBody = db.Column(db.String(255))
    criticPublication = db.Column(db.String(120))
    datePosted = db.Column(db.String(120))

    def __repr__(self):
        cleaned = {}
        for key, val in self.__dict__:
            if(key[0] != '_'):
                cleaned[key] = val
        return json.dumps(cleaned)

    def to_dict(self):
        cleaned = {}
        for key in self.__dict__:
            if(key[0] != '_'):
                cleaned[key] = self.__dict__[key]
        return cleaned