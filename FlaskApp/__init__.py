from configparser import ConfigParser

from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    urlconf = 'config/config.ini'
    config = ConfigParser()
    config.read(urlconf)
    secret_key = config['flask']['secret_key']
    app.secret_key = secret_key
    app.config['MAIL_SERVER'] = config['email']['MAIL_SERVER']
    app.config['MAIL_PORT'] = config['email']['MAIL_PORT']
    app.config['MAIL_USE_TLS'] = bool(int(config['email']['MAIL_USE_TLS']))
    app.config['MAIL_USE_SSL'] = bool(int(config['email']['MAIL_USE_SSL']))
    app.config['MAIL_USERNAME'] = config['email']['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = config['email']['MAIL_PASSWORD']
    app.config['MAIL_DEFAULT_SENDER'] = config['email']['MAIL_DEFAULT_SENDER']
    mail.init_app(app)
    import routes
    app.register_blueprint(routes.pages)
    app.register_blueprint(routes.api)
    return app

