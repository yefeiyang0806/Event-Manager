from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField, SelectMultipleField, widgets
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
# from werkzeug.security import check_password_hash
from app.models import User, Event, Menu, Role_menu, Role
import datetime


def unique_menu_name(form, field):
	existed_name = db.session.query(Menu).filter(Menu.menu_name == field.data).first()
	if existed_name is not None:
		raise ValidationError('Menu name already existed.')


def unique_menu_id(form, field):
	existed_id = db.session.query(Menu).filter(Menu.menu_id == field.data).first()
	if existed_id is not None:
		raise ValidationError('Menu ID already existed.')


class MenuCreationForm(Form):
	menu_name = StringField('Menu Name', validators=[InputRequired(), unique_menu_name, Length(max=40)])
	menu_id = StringField('Menu ID', validators=[InputRequired(), unique_menu_id, Length(max=10)])
	category_name = StringField('Category Name', validators=[InputRequired(), Length(max=40)])
	category_id = StringField('Category ID', validators=[InputRequired(), Length(max=40)])
	url = StringField('Assigned URL', validators=[InputRequired(), Length(max=100)])