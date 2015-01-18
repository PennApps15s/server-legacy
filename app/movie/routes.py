from flask import Blueprint, request, g

from app import db
from app.movie.models import Movie
from app.user.decorators import requires_login
from app.review.models import Review
from app.user.models import User

from datetime import datetime
import json

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movie')

COLUMNS_FOR_FEED = ['id', '"Title"', '"imdbRating"', '"Poster"', '"Year"', '"Rating"']
UNIVERSAL_FILTERS = '''
        movies."Rating" IN (
            'G', 'PG', 'PG-13', 'R', 'TV-PG'
        )
        AND (movies."Year" > 2004)
        AND (movies."imdbRating" > 5)
    '''

@movies_blueprint.route('/feed/', methods=['GET'])
@requires_login
def get_movie_feed():
    most_voted_results = db.engine.execute('''
        SELECT ''' + ', '.join(COLUMNS_FOR_FEED) + '''
        FROM movies 
        WHERE ''' + UNIVERSAL_FILTERS + '''
        AND movies.id NOT IN (
            SELECT reviews."movieId" 
            FROM reviews 
            WHERE reviews."userId" = ''' + str(g.user.id) + '''
        )
        ORDER BY movies."imdbVotes" DESC
        LIMIT 12
    ''')

    highest_rated_results = db.engine.execute('''
        SELECT ''' + ', '.join(COLUMNS_FOR_FEED) + '''
        FROM movies 
        WHERE ''' + UNIVERSAL_FILTERS + '''
        AND movies.id NOT IN (
            SELECT reviews."movieId" 
            FROM reviews 
            WHERE reviews."userId" = ''' + str(g.user.id) + '''
        )
        ORDER BY movies."imdbRating" DESC
        LIMIT 12
    ''')

    feed_movies = []
    for row in most_voted_results:
        data = {}
        for i, cell in enumerate(row):
            data[COLUMNS_FOR_FEED[i].replace('"', '')] = cell
        feed_movies.append(data)
    for row in highest_rated_results:
        data = {}
        for i, cell in enumerate(row):
            data[COLUMNS_FOR_FEED[i].replace('"', '')] = cell
        feed_movies.append(data)

    return json.dumps(feed_movies), 200, {'Content-Type': 'application/json'}

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
        datePosted=str(datetime.now())
    )
    db.session.add(created_review)
    db.session.commit()
    
    return "OK", 200