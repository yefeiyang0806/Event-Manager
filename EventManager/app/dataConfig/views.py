from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from sqlalchemy.exc import IntegrityError
# from .forms import CreateRoleForm
from ..models import User, Role, Role_menu, Menu, Resource
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random, json

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


# Responsible for managing resources. Listing all resources.
@dataConfig.route('/menus_and_roles', methods = ['GET', 'POST'])
@login_required
def m_r_index():
    menus_by_cat = []
    cat_bucket = dict()
    cat_menus = []
    menus_objs = db.session.query(Menu).order_by(Menu.category_name).all()
    current_category = menus_objs[0].category_name
    for mo in menus_objs:
        if current_category != mo.category_name:
            cat_bucket['menus'] = cat_menus
            menus_by_cat.append(cat_bucket)
            cat_bucket = dict()
            cat_menus = []
            current_category = mo.category_name
        cat_bucket['category'] = mo.category_name
        menu_obj = dict()
        assigned_roles = getRoleNames(mo)
        menu_obj['menu'] = mo
        menu_obj['roles'] = assigned_roles
        cat_menus.append(menu_obj)
    cat_bucket['menus'] = cat_menus
    menus_by_cat.append(cat_bucket)
    roles = db.session.query(Role).all()

    return render_template('dataConfig/menus_and_roles_index.html', menus_by_cat=menus_by_cat, \
        roles=roles, full_name=full_name, status=status, menu_categories=menu_categories)


#Update and return new rolenames based on the provided menu id through Ajax.
@dataConfig.route('/update_rolenames_ajax')
@login_required
def ajax_rolenames_update():
    modified_role = request.args.get('modified_role', None)
    op_type = request.args.get('op_type', None)
    menu_id = request.args.get('menu_id', None)
    # print(modified_role)
    # print(op_type=='add')
    # print(menu_id)
    if modified_role is None:
        return jsonify({'error':'No proper role has been provided.'})
    if op_type is None:
        return jsonify({'error':'No operation type has been provided.'})

    if menu_id is not None:
        update_role_menu(modified_role, menu_id, op_type)
        mo = db.session.query(Menu).filter(Menu.menu_id == menu_id).first()
        assigned_roles = getRoleNames(mo)
        return json.dumps(assigned_roles)
    else:
        category_name = request.args.get('category', None)
        if category_name is not None:
            # Add or remove a role for the whole menu group.
            menu_ids = db.session.query(Menu.menu_id).filter(Menu.category_name == category_name).all()
            menu_ids = [mi[0] for mi in menu_ids]
            print(menu_ids)
            for m_id in menu_ids:
                update_role_menu(modified_role, m_id, op_type)
            # Send new lists of roles back to front-end.
            result = []
            menus = db.session.query(Menu).filter(Menu.category_name == category_name).all()
            for mo in menus:
                menu_roles = dict()
                menu_roles['menu_id'] = mo.menu_id
                menu_roles['assigned_roles'] = getRoleNames(mo)
                result.append(menu_roles)
            return json.dumps(result)
        else:
            return jsonify({'error':'No category names or menu IDs defined.'})


#Given menu object, return the name of related roles.
def getRoleNames(mo):
    assigned_roles = []
    relations = db.session.query(Role_menu).filter(Role_menu.menu_id == mo.menu_id).order_by(Role_menu.role_id).all()
    role_ids = [r.role_id for r in relations]
    # print(role_ids)
    for ri in role_ids:
        assigned_roles.append(db.session.query(Role.rolename).filter(Role.role_id == ri).first()[0])
    return assigned_roles


#Given menu id, role id and operation type, update Role_menu table.
def update_role_menu(modified_role, menu_id, op_type):
    mo = db.session.query(Menu).filter(Menu.menu_id == menu_id).first()
    if_existed = db.session.query(Role_menu).filter(Role_menu.role_id == modified_role)\
        .filter(Role_menu.menu_id == mo.menu_id).first()
    if op_type == 'add':
        if if_existed is None:
            new_role_menu = Role_menu(modified_role, mo.menu_id, g.user.user_id)
            db.session.add(new_role_menu)
            db.session.commit()
        else:
            print('Relation already existed.')
    elif op_type == 'remove':
        if if_existed is not None:
            db.session.delete(if_existed)
            db.session.commit()
        else:
            print('Relation not exists yet.')


#Refresh the global variable before every request
@dataConfig.before_request
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
    for m in middles:
        certain_menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        if certain_menu.category_id not in category_ids:
            category_ids.append(certain_menu.category_id)
            cat_grouped_menus.append(certain_menu)
    for c in cat_grouped_menus:
        c_menus = list()
        cat = dict()
        cat['category_id'] = c.category_id
        cat['category_name'] = c.category_name
        menus = db.session.query(Menu).filter(Menu.category_id == c.category_id).all()
        for m in menus:
            each_menu = dict()
            each_menu['menu_id'] = m.menu_id
            each_menu['menu_name'] = m.menu_name
            each_menu['url'] = m.url
            c_menus.append(each_menu)
        cat['menus'] = c_menus
        menu_categories.append(cat)

    # print (menu_categories)
    return menu_categories