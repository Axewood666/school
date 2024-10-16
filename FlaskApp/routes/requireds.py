from flask import redirect, url_for, flash
from flask_login import current_user


def teacher_required(f):
    def decorated_function(*args, **kwargs):
        if current_user.user_type != 'teacher':
            flash('Login as teacher')
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)

    return decorated_function
