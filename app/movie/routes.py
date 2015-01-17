from flask import Blueprint

from app import db
from app.movie.models import Movie

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movie')

@movies_blueprint.route('/<movie_id>/like', methods=["POST"])
def like_movie(movie_id):
    return str(user), 200, {'Content-Type': 'application/json'}