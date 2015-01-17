from functools import wraps

from flask import g, flash, redirect, url_for, request

def requires_login(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			return "Error: user must be logged in", 401
		return f(*args, **kwargs)
	
	return decorated_function