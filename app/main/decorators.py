from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.isAdmin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def gamer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        en=current_user
        if current_user.isAdmin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function