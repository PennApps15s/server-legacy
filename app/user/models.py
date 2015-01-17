from app import db
import json
from marshmallow import Serializer

class UserSerializer(Serializer):
    class Meta:
        fields = ('id', 'name', 'email', 'isCritic', 'bio', 'criticPublication', 'highest_review', 'lowest_review', 'average_review')

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
        return UserSerializer(self).data

    def to_json(self):
        return json.dumps(UserSerializer(self).data)

    def to_json_response(self):
        return json.dumps(UserSerializer(self).data), 200, {'Content-Type': 'application/json'}