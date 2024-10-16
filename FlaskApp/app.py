import db_package as db
from flask import Flask
from configparser import ConfigParser
from flask_login import LoginManager
import routes

app = Flask(__name__)
app.register_blueprint(routes.pages.pages)
app.register_blueprint(routes.api.api)
urlconf = 'config/config.ini'
config = ConfigParser()
config.read(urlconf)
secret_key = config['flask']['secret_key']
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'pages.login'


@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, id_ = user_id.split('_')
        user = db.model.User.get_user_by_id(id_, user_type)
        return user
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    app.run()
