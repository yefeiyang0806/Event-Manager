from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'basic.index'
Bootstrap(app)
CsrfProtect(app)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

from app import models
from .basic.views import basic
from .event.views import event

# Register blueprint basic and event.
# Basic contains the functions of normal users, while event contains actions related to events.
app.register_blueprint(basic, url_prefix='')
app.register_blueprint(event, url_prefix='/event')