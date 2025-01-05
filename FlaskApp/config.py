from configparser import ConfigParser

from FlaskApp.db_package.model import SchoolDB


def set_app_config(app):
    urlconf = 'config.ini'
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

def connect_db():
    urlconf = 'config.ini'
    config = ConfigParser()
    config.read(urlconf)
    user_db = config['login_db']['user_db']
    password_db = config['login_db']['password_db']
    name_db = config['login_db']['database_name']
    host_db = config['login_db']['host_db']
    port_db = config['login_db']['port_db']
    return SchoolDB(name_db, user_db, password_db, host_db, port_db)