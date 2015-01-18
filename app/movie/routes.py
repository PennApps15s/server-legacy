from flask import Blueprint

from app import db
from app.movie.models import Movie
from app.user.decorators import requires_login

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movie')

@movies_blueprint.route('/feed', methods=['GET'])
@requires_login
def get_movie_feed():
    result = db.engine.execute('''SELECT movies.id
        FROM movies 
        WHERE movies.id 
        NOT IN (
            SELECT reviews."movieId" 
            FROM reviews 
            WHERE reviews."userId" = ''' + g.user.id + ')')

    print result

    return str(user), 200, {'Content-Type': 'application/json'}

@movies_blueprint.route('/<movie_id>/like', methods=['POST'])
def like_movie(movie_id):
    return str(user), 200, {'Content-Type': 'application/json'}