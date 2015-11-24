from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
Bootstrap(app)
CsrfProtect(app)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models
