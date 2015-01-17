import os
import sys

from flask import Flask, render_template
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

from app.user.routes import mod as usersModule
app.register_blueprint(usersModule)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)