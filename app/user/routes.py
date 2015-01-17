from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.user.models import User
from app.user.decorators import requires_login

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
        name=request.form['name'],
        email=request.form['email'],
        password= bcrypt.hashpw( request.form['password'].encode('utf-8'), bcrypt.gensalt() ),
        session = token
    )
    db.session.add(created_user)
    db.session.commit()


    user = User.query.filter(User.email == request.form['email'])[0]
    
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


@mod.route('/login', methods=['POST'])
def login():
    user = User.query.filter(User.email == request.form['email'])[0]
    hashed = user.password.encode('utf-8')
    if bcrypt.hashpw(request.form['password'].encode('utf-8'), hashed) == hashed:
        return json.dumps({
            'session': gen_session( user ),
            'user': user.to_dict()
        }), 200, {'Content-Type': 'application/json'}
    else:
        return 'Incorrect password', 401

@mod.route('/me', methods=["GET"])
def get_me():
    return json.dumps(g.user.to_dict()), 200, {'Content-Type': 'application/json'}

