from flask import Blueprint

from app import db
from app.review.models import Review

reviews_blueprint = Blueprint('reviews', __name__, url_prefix='/review')

@reviews_blueprint.route('/', methods=["POST"])
def create_review():
    review = Review(
            userId = request.form['userId'],
            movieId = request.form['movieId'],
            score = request.form['score'],
            reviewBody = request.form['reviewBody'],
            publicationTitle = request.form['publicationTitle'],
            datePosted = request.form['datePosted']
        )
    db.session.add(review)
    db.session.commit()
    return str(review), 200, {'Content-Type': 'application/json'}