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

'''
not auth - могут отправить резюме(в планах)
student - /(! Переделать редирект с логина)могут смотреть свой профиль. 
    /В профиле список класса(препод названия одноклассники с мылом номером), список оценок, свои данные.
teacher - /может пользоваться вкладкой student и своим профилем. В профиле инфа + выставить оценку(уже есть).
    Во вкладке student возможность смотреть студентов по фио(оценки) и названиям классов(список студентов класса по нажатию вызывать функцию оценки либо ввод в инпут)(ЛЧ номер почта)
staff - может пользоваться вкладкой student(будет фул ЛЧ о студентах) и teacher и своим профилем
    вкладка teacher(уже готова, требуется доработка) 
        с полным доступом к преподам(будет список и по нему можно будет обратиться к определенному преподу либо ввести в инпут)
    Профиль - добавление студента(автогенерация профиля с хэшированием пароля отправка пароля на почту),
        добавление препода(автогенерация профиля с хэшированием пароля отправка пароля на почту),
         рассмотрение резюме и его перенос в форму добавление студента, препода(в планах)
'''
