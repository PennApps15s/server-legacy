from app import db
import json
from marshmallow import Serializer


class MovieSerializer(Serializer):
    class Meta:
        fields = (
            'id',
            'imdbId',
            'movieTitle',
            'genre',
            'runtime',
            'director',
            'writer',
            'actors',
            'rated',
            'releaseYear',
            'releaseDate',
            'plot',
            'poster',
            'language',
            'country',
            'awards',
            'metascore',
            'imdbRating',
            'imdbVotes'
        )

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
        return self.to_json()

    def to_dict(self):
        return MovieSerializer(self).data

    def to_json(self):
        return json.dumps(MovieSerializer(self).data)

    def to_json_response(self):
        return json.dumps(MovieSerializer(self).data), 200, {'Content-Type': 'application/json'}