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
full_name = ''
status = ''
menu_categories = list()

# Responsible for creating Roles.
@role.route('/create', methods = ['GET', 'POST'])
@login_required
def create_role():
    create_by = g.user.full_name
    menus = menus_of_role()
    form = CreateRoleForm()
    if form.validate_on_submit():
        temp = Role(form.rolename.data, form.description.data, create_by)
        db.session.add(temp)
        db.session.commit()
        return redirect(url_for('role.manage_roles'))
    return render_template("role/create_role.html", form=form, full_name=full_name, menu_categories=menu_categories, status=status)

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
            return render_template("role/modify_role.html", form=form, menu_categories=menu_categories, full_name=full_name, status=status, role_uuid=role_uuid)

    # if role.is_created_by(g.user.uuid):
    else:
        form.rolename.data = role.rolename
        form.description.data = role.description         
        return render_template("role/modify_role.html", form=form, menu_categories=menu_categories, full_name=full_name, status=status, role_uuid=role_uuid)
    return redirect(url_for("role.manage_roles"))


#Show all the available events in the website.
#Once finished, should only show approved events
@role.route('/manage')
@login_required
def manage_roles():
    menus = menus_of_role()
    roles = db.session.query(Role).all()
    return render_template('role/manage_roles.html', roles=roles, full_name=full_name, status=status, menu_categories=menu_categories)


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Refresh the global variable before every request
@role.before_request
def before_request():
    g.user = current_user
    global full_name, status, menu_categories
    if hasattr(g.user, 'full_name'):
        full_name = g.user.full_name
    if hasattr(g.user, 'status'):
        status = g.user.status
        menu_categories = menus_of_role()


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menu_categories = list()
    cat_grouped_menus = list()
    category_ids = list()
    menu_ids = list()
    for m in middles:
        certain_menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menu_ids.append(certain_menu.menu_id)
        if certain_menu.category_id not in category_ids:
            category_ids.append(certain_menu.category_id)
            cat_grouped_menus.append(certain_menu)
    for c in cat_grouped_menus:
        c_menus = list()
        cat = dict()
        cat['category_id'] = c.category_id
        cat['category_name'] = c.category_name
        menus = db.session.query(Menu).filter(Menu.category_id == c.category_id).filter().all()
        for m in menus:
            if m.menu_id in menu_ids:
                each_menu = dict()
                each_menu['menu_id'] = m.menu_id
                each_menu['menu_name'] = m.menu_name
                each_menu['url'] = m.url
                c_menus.append(each_menu)
        cat['menus'] = c_menus
        menu_categories.append(cat)

    # print (menu_categories)
    return menu_categories