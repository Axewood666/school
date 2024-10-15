from flask import redirect, url_for
from flask_login import current_user


def teacher_required(f):
    def decorated_function(*args, **kwargs):
        if current_user.user_type != 'teacher':
            return redirect(url_for('pages.Main'))
        return f(*args, **kwargs)

    return decorated_function
