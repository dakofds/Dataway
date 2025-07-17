from flask import session, redirect, url_for
from functools import wraps
from backend.models import Board, Topic

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username') or not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        name = session.get("username")
        verify = db.query(User).filter_by(name=name, is_staff=True).first()
        if not verify:
            return redirect(url_for('board.read_root', board='home'))
        return f(*args, **kwargs) 
    return decorated_function 
