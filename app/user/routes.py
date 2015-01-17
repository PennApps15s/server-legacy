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
    token = random_uiud().hex
    user.session = token
    db.session.add(user)
    db.session.commit()
    return token


@mod.before_request
def before_request():
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

@mod.route('/', methods=["POST"])
def create_user():
    token = random_uuid().hex
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        password= gen_session(),
        token = token
    )
    db.session.add(user)
    db.session.commit()
    return str(user), 200, {'Content-Type': 'application/json'}

@mod.route('/login', methods=['POST'])
def login():
    # Untested
    hashed = user.password.encode('utf-8')
    if bcrypt.hashpw(password, hashed) == hashed:
        return json.dumps({
            'session': create_token( user.id ),
            'user': user.to_dict()
        }), 200, jsonType
    else:
        return 'Incorrect password', 401

@mod.route('/', methods=["GET"])
def get_all():
    q = User.query.all()
    result = []
    for item in q:
        result.append(item.to_dict())
    return json.dumps(result), 200, {'Content-Type': 'application/json'}
