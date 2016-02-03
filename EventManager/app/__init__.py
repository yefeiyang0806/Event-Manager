from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail
# from sqlalchemy.exc import IntegrityError

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
from .topic.views import topic
from .role.views import role
from .upload.views import upload
from .dataConfig.views import dataConfig

# Register blueprint basic and event.
# Basic contains the functions of normal users, while event contains actions related to events.
app.register_blueprint(basic, url_prefix='')
app.register_blueprint(topic, url_prefix='/topic')
app.register_blueprint(role, url_prefix='/role')
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(dataConfig, url_prefix='/dataConfig')