from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.user.models import User
from app.user.decorators import requires_login

import json

mod = Blueprint('users', __name__, url_prefix='/user')

# @mod.before_request
# def before_request():
#   g.user = None
#   if 'user_id' in session:
#     g.user = User.query.get(session['user_id'])

@mod.route('/signup', methods=["GET"])
def create_user():
	user = User(name="Peter", email="test@example.com", password="test")
	db.session.add(user)
	db.session.commit()
	return str(user)

@mod.route('/login', methods=['POST'])
def login():
	return;

@mod.route('/', methods=["GET"])
def get_all():
	q = User.query.all()
	result = []
	for item in q:
		result.append(item.to_dict())
	return json.dumps(result), 200, {'Content-Type': 'application/json'}
