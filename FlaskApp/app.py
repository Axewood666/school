import db_package as db
from flask import render_template
from flask_login import LoginManager
from __init__ import create_app

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'pages.login'


@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, id_ = user_id.split('_')
        user = db.User.get_user_by_id(id_, user_type, db.schoolDB)
        return user
    except:
        return None


@app.errorhandler(404)
def error404(error):
    return render_template('error/error404.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
