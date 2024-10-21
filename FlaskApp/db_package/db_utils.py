from configparser import ConfigParser
from .model import SchoolDB, User

urlconf = 'config/config.ini'
config = ConfigParser()
config.read(urlconf)
user_db = config['login_db']['user_db']
password_db = config['login_db']['password_db']
name_db = config['login_db']['database_name']
host_db = config['login_db']['host_db']
schoolDB = SchoolDB(name_db, user_db, password_db, host_db)
