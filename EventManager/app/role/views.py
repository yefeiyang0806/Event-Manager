from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateRoleForm
from ..models import User, Role, Role_menu, Menu
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


role = Blueprint('role', __name__)


# Responsible for creating Roles.
@role.route('/create', methods = ['GET', 'POST'])
@login_required
def create_role():
    first_name = g.user.first_name
    last_name = g.user.last_name
    create_by = last_name + ' ' + first_name
    status = g.user.status
    menus = menus_of_role()
    form = CreateRoleForm()
    if form.validate_on_submit():
        temp = Role(form.rolename.data, form.description.data, create_by)
        db.session.add(temp)
        db.session.commit()
        return redirect(url_for('role.manage_roles'))
    return render_template("role/create_role.html", form=form, first_name=first_name, menus=menus, status=status)

#Responsible for deleting existing roles.
#Called by jquery in role.view_event.html and basic.member.html
@role.route('/delete')
@login_required
def delete_role():
    role_uuid = request.args.get('role_uuid')
    role = db.session.query(Role).filter(Role.uuid == role_uuid).first()
    print ("delete!!!")
    print ("ready to remove the role!")
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for("role.manage_roles"))

#Render to the events modification page.
#If method is GET, show the event info on the form for the user to modify
#If method is POST, do the validation and update the event 
#ATTENTION: The validation is not working currently
@role.route('/modify/<role_uuid>', methods = ['GET', 'POST'])
@login_required
def modify_role(role_uuid):
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    form = CreateRoleForm()
    role = Role.query.get(role_uuid)
    if request.method == 'POST':
        print("POST received")
        if form.validate_on_submit():
            #event_id = request.form.get('event_id')
            role.rolename = form.rolename.data
            role.description = form.description.data
            # first_name = g.user.first_name
            # last_name = g.user.last_name
            # role.create_by = last_name + ' ' + first_name
            db.session.commit()
            return redirect(url_for("role.manage_roles"))
        else:
            print ("Not validated") 
            return render_template("role/modify_role.html", form=form, menus=menus, first_name=first_name, status=status, role_uuid=role_uuid)

    # if role.is_created_by(g.user.uuid):
    else:
        form.rolename.data = role.rolename
        form.description.data = role.description         
        return render_template("role/modify_role.html", form=form, menus=menus, first_name=first_name, status=status, role_uuid=role_uuid)
    return redirect(url_for("role.manage_roles"))


#Show all the available events in the website.
#Once finished, should only show approved events
@role.route('/manage')
@login_required
def manage_roles():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    roles = db.session.query(Role).all()
    return render_template('role/manage_roles.html', roles=roles, first_name=first_name, status=status, menus=menus)


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Refresh the global variable before every request
@role.before_request
def before_request():
    g.user = current_user


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).get(m.menu_id)
        menus.append(menu)
    print (menus)
    return menus