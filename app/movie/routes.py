from flask import Blueprint, request, g

from app import db
from app.movie.models import Movie
from app.user.decorators import requires_login
from app.review.models import Review

from datetime import datetime

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movie')

@movies_blueprint.route('/<movie_id>/', methods=["GET"])
@requires_login
def get_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id)
    if not movie.count() == 1:
        return "Movie not found", 404

    return movie.all()[0].to_json_response()

@movies_blueprint.route('/<movie_id>/review', methods=["POST"])
@requires_login
def like_movie(movie_id):
    if not Movie.query.get(movie_id):
        return "Movie not found", 404

    action = request.json['action']

    action_code = 0
    if action == 'like':
        action_code = 1
    elif action == 'unlike':
        action_code = -1
    print g.user.id, movie_id, action_code, datetime
    created_review = Review(
        userId= g.user.id,
        movieId=movie_id,
        score=action_code,
        datePosted=str(datetime)
    )
    db.session.add(created_review)
    db.session.commit()
    
    return "OK", 200