from flask import Blueprint

from app import db
from app.review.models import Review

reviews_blueprint = Blueprint('reviews', __name__, url_prefix='/review')

@movies_blueprint.route('/', methods=["POST"])
def create_review():
    review = Review(
            userId = request.form['userId'],
            reviewId = request.form['reviewId'],
            score = request.form['score'],
            reviewBody = request.form['reviewBody'],
            publicationTitle = request.form['publicationTitle'],
            datePosted = request.form['datePosted']
        )
    db.session.add(user)
    db.session.commit()
    return str(user), 200, {'Content-Type': 'application/json'}