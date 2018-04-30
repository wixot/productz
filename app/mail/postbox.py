from threading import Thread
from flask import current_app, render_template
from flask_mail import Message, Mail


def send_mail_async(app, msg):
    with app.app_context():
        mail = Mail(app)
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    send_mail_async(app, msg)
    thr = Thread(target=send_mail_async, args=[app, msg])
    thr.start()
    return None