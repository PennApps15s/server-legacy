import os
import sys

from flask import Flask, render_template, g, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app) 

@app.errorhandler(404)
def not_found(error):
    return "404 ERROR"

@app.route('/')
def main():
    return "Working!"

@app.before_request
def make_user():
    from app.user.models import User
    g.user = None
    print("pre")
    if 'session' in request.headers:
        results = User.query.filter(User.session == request.headers['session'])
        if results.count() == 1:
            g.user = results[0]
            print("found", g.user)
        else:
            print("Error: Duplicate ")


from app.user.routes import mod as usersModule
app.register_blueprint(usersModule)

from app.review.routes import reviews_blueprint
app.register_blueprint(reviews_blueprint)

from app.movie.routes import movies_blueprint
app.register_blueprint(movies_blueprint)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)