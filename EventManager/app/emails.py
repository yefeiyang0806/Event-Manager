from flask.ext.mail import Message
from flask import render_template
from threading import Thread
from config import ADMINS
from .decorators import async
from app import mail, app


@async
def send_async_email(msg):
	with app.app_context():
		mail.send(msg)

 
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    print('Sender in emails')
    print(sender)
    send_async_email(msg)