from flask import render_template

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from FlaskApp.config import set_app_config, connect_db
app = Flask(__name__)

set_app_config(app)

mail = Mail()
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'pages.login'

schoolDB = connect_db()


from FlaskApp.routes.pages import pages
from FlaskApp.routes.api import api

app.register_blueprint(pages)
app.register_blueprint(api)


@app.errorhandler(404)
def error404(error):
    return render_template('error/error404.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
