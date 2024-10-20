from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type != 'teacher':
            flash('Login as teacher')
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)

    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type != 'student':
            flash('Login as student')
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)

    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type != 'staff':
            flash('Login as staff')
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)

    return decorated_function

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type != 'staff' and current_user.user_type != 'teacher':
            flash('Login as employee')
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)

    return decorated_function
