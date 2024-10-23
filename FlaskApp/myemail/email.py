from flask_mail import Message
from flask import current_app, Flask
from threading import Thread
from FlaskApp import mail, create_app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(user, login, password):
    try:
        app = current_app._get_current_object()
        msg = Message(f"Welcome in our school {user['fio']}",
                      recipients=[user['mail']])
        msg.body = f"Your login {login} password {password}"
        mail.send(msg)
        Thread(target=send_async_email, args=(app, msg)).start()
    except Exception as e:
        print(str(e))
