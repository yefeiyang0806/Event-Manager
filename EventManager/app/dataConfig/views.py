from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
# from .forms import CreateRoleForm
from ..models import User, Role, Role_menu, Menu, Resource
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random

dataConfig = Blueprint('dataConfig', __name__)
full_name = ''
status = ''
menu_categories = list()


# Responsible for managing resources. Listing all resources.
# @dataConfig.route('/resource', methods = ['GET', 'POST'])
# @login_required
# def resource_index():
# 	resources = db.session.query(Resource).all()
# 	return render_template("dataConfig/resource/index.html", full_name=full_name, status=status, menus=menus)





#Refresh the global variable before every request
@topic.before_request
def before_request():
    g.user = current_user
    global full_name, status
    full_name = g.user.full_name
    status = g.user.status


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menus.append(menu)
    #print (menus)
    return menus