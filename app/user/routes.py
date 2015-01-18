from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.user.models import User
from app.review.models import Review 
from app.user.decorators import requires_login
from app.user.criticList import get_critics

import json
from uuid import uuid4 as random_uuid
import bcrypt

mod = Blueprint('users', __name__, url_prefix='/user')

def gen_session(user):
    token = random_uuid().hex
    user.session = token
    db.session.add(user)
    db.session.commit()
    return token

@mod.route('/', methods=["POST"])
def create_user():
    token = random_uuid().hex
    created_user = User(
        name=request.json['name'],
        email=request.json['email'],
        password= bcrypt.hashpw( request.json['password'].encode('utf-8'), bcrypt.gensalt() ),
        session = token
    )
    db.session.add(created_user)
    db.session.commit()


    user = User.query.filter(User.email == request.json['email'])[0]
    
    return json.dumps({
        'session': token,
        'user': user.to_dict()
    }), 200, {'Content-Type': 'application/json'}

@mod.route('/', methods=["GET"])
def get_all():
    q = User.query.all()
    result = []
    for item in q:
        result.append(item.to_dict())
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@mod.route('/login/', methods=['POST'])
def login():
    user = User.query.filter(User.email == request.json['email'])[0]
    hashed = user.password.encode('utf-8')
    if bcrypt.hashpw(request.json['password'].encode('utf-8'), hashed) == hashed:
        return json.dumps({
            'session': gen_session( user ),
            'user': user.to_dict()
        }), 200, {'Content-Type': 'application/json'}
    else:
        return 'Incorrect password', 401

@mod.route('/<user_id>/', methods=["GET"])
@requires_login
def get_user(user_id):
    if user_id == 'me':
        return g.user.to_json_response()

    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    return user.to_json_response()

@mod.route('/<user_id>/reviews', methods=["GET"])
@requires_login
def get_user_likes(user_id):
    if user_id == 'me':
        user_id = g.user.id

    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    results = []
    for r in Review.query.filter(Review.userId == user_id).all():
        results.append(r.to_dict())

    return json.dumps(results), 200, {'Content-Type': 'application/json'}

@mod.route('/<user_id>/sharedLikes', methods=["GET"])
@requires_login
def get_user_shared_likes(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    sql = """
        SELECT movies.id, "Title", "Year", "Rating", "Poster" FROM reviews
        LEFT JOIN movies ON "movieId"=movies.id
        WHERE "userId" = %s AND "movieId" IN
            (SELECT "movieId" FROM reviews
             WHERE "userId" = %s AND score=1)
        """ % (user_id, g.user.id)

    columns = ['id', 'Title', 'Year', 'Rating', 'Poster']
    result = []
    for row in db.engine.execute(sql):
        data = {}
        for i, cell in enumerate(row):
            data[ columns[i].replace('"', '') ] = cell
        result.append(data)

    return json.dumps(result), 200, {'Content-Type': 'application/json'} 

@mod.route('/<user_id>/favorite', methods=["GET"])
@requires_login
def get_user_favorite(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    sql = """
        SELECT movies.id, "Title", "Year", "Rating", "Poster", "metacriticScore", "reviewBody" FROM reviews
        LEFT JOIN movies ON "movieId"=movies.id
        WHERE "userId" = %s AND "metacriticScore" > 90
            AND "movieId" NOT IN
            (SELECT "movieId" FROM reviews
             WHERE "userId" = %s)
        ORDER BY "metacriticScore" DESC
        LIMIT 18
        """ % (user_id, g.user.id)

    columns = ['id', 'Title', 'Year', 'Rating', 'Poster', 'metacriticScore', 'reviewBody']
    result = []
    for row in db.engine.execute(sql):
        data = {}
        for i, cell in enumerate(row):
            data[ columns[i].replace('"', '') ] = cell
        result.append(data)

    return json.dumps(result), 200, {'Content-Type': 'application/json'} 

@mod.route('/<user_id>/recent', methods=["GET"])
@requires_login
def get_user_recent(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    sql = """
        SELECT movies.id, "Title", "Year", "Rating", "Poster", "metacriticScore", "reviewBody" FROM reviews
        LEFT JOIN movies ON "movieId"=movies.id
        WHERE "userId" = %s
            AND "movieId" NOT IN
            (SELECT "movieId" FROM reviews
             WHERE "userId" = %s)
        ORDER BY "Year" DESC
        LIMIT 18
        """ % (user_id, g.user.id)

    columns = ['id', 'Title', 'Year', 'Rating', 'Poster', 'metacriticScore', 'reviewBody']
    result = []
    for row in db.engine.execute(sql):
        data = {}
        for i, cell in enumerate(row):
            data[ columns[i].replace('"', '') ] = cell
        result.append(data)

    return json.dumps(result), 200, {'Content-Type': 'application/json'} 


@mod.route('/criticList/', methods=["GET"])
@requires_login
def get_user_critics():
    likes = Review.query.filter(Review.userId == g.user.id).all()
    if len(likes) < 10:
        return "User needs more likes", 409

    results = []
    for r in get_critics(g.user, likes):
        results.append(r)

    if len(results) == 0:
        return "User needs more likes", 409        

    return json.dumps(results), 200, {'Content-Type': 'application/json'}

