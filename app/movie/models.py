from app import db
import json

class Movie(db.Model):
    __tablename__ = 'movies'
    id              = db.Column(db.Integer, primary_key=True)
    imdbId          = db.Column(db.String(120))

    movieTitle      = db.Column(db.String(255))
    genre           = db.Column(db.String(255))
    runtime         = db.Column(db.String(255))
    director        = db.Column(db.String(255))
    writer          = db.Column(db.String(255))
    actors          = db.Column(db.String(255))
    rated           = db.Column(db.String(255))
    releaseYear     = db.Column(db.Integer)
    releaseDate     = db.Column(db.String(255))
    plot            = db.Column(db.Text)
    poster          = db.Column(db.String(255))
    language        = db.Column(db.String(255))
    country         = db.Column(db.String(255))
    awards          = db.Column(db.String(255))

    metascore       = db.Column(db.Integer)
    imdbRating      = db.Column(db.Integer)
    imdbVotes       = db.Column(db.Integer)


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