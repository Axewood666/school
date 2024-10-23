from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

from __init__ import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    try:
        app = current_app._get_current_object()
        msg = Message(subject, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=send_async_email, args=(app, msg)).start()
    except Exception as e:
        print(str(e))


def send_email_for_student(user, login, password):
    subject = "Welcome in our school ^-^"
    recipients = [user['mail']]
    html_body = render_template('/mails/for-new-student.html', user=user['fio'],
                                login=login, password=password)
    text_body = render_template('/mails/for-new-student.txt', user=user['fio'],
                                login=login, password=password)
    send_email(subject, recipients, text_body, html_body)


def send_email_for_teacher(user, login, password):
    subject = "Welcome in our school ^-^"
    recipients = [user['mail']]
    html_body = render_template('/mails/for-new-teacher.html', user=user['fio'],
                                login=login, password=password)
    text_body = render_template('/mails/for-new-teacher.txt', user=user['fio'],
                                login=login, password=password)
    send_email(subject, recipients, text_body, html_body)
