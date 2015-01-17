from app import db
import json
from marshmallow import Serializer


class MovieSerializer(Serializer):
    class Meta:
        fields = (
            'id',
            'imdbID',
            'Title',
            'Year',
            'Rating',
            'Runtime',
            'Genre',
            'Released',
            'Director',
            'Writer',
            'Cast',
            'Metacritic',
            'imdbRating',
            'imdbVotes',
            'Poster',
            'Plot',
            'FullPlot',
            'Language',
            'Country',
            'Awards',
            'lastUpdated'
        )

class Movie(db.Model):
    __tablename__ = 'movies'
    id              = db.Column(db.Integer, primary_key=True)
    imdbID          = db.Column(db.String(120))
    Title           = db.Column(db.String(255))
    Year            = db.Column(db.Integer)
    Rating          = db.Column(db.String(255))
    Runtime         = db.Column(db.String(255))
    Genre           = db.Column(db.String(255))
    Released        = db.Column(db.String(255))
    Director        = db.Column(db.String(255))
    Writer          = db.Column(db.String(255))
    Cast            = db.Column(db.Text)
    Metacritic      = db.Column(db.Integer)
    imdbRating      = db.Column(db.Float)
    imdbVotes       = db.Column(db.Integer)
    Poster          = db.Column(db.String(510))
    Plot            = db.Column(db.Text)
    FullPlot        = db.Column(db.Text)
    Language        = db.Column(db.String(255))
    Country         = db.Column(db.String(255))
    Awards          = db.Column(db.Text)
    lastUpdated     = db.Column(db.Date)


    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return MovieSerializer(self).data

    def to_json(self):
        return json.dumps(MovieSerializer(self).data)

    def to_json_response(self):
        return json.dumps(MovieSerializer(self).data), 200, {'Content-Type': 'application/json'}