# -*- coding: utf-8 -*-
from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import LoginForm, JoinForm, RetrievePwdForm, PwdResetForm
from ..models import User, Topic, Menu, Role, Role_menu, Content, Format, ResourceType, Resource, Event, EventAttender
from ..emails import send_email
from werkzeug.security import generate_password_hash


import random, json, datetime


basic = Blueprint('basic', __name__)
full_name = ''
status = ''
menu_categories = list()


#Home page of the website, ask for login
#Also provide link to register and forgot password
#Remember me is used to keep the login status
@basic.route('/')
@basic.route('/index', methods = ['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('basic.logged_in'))

    form = LoginForm()
    email_form = RetrievePwdForm()
    next = request.args.get('next')
    if form.validate_on_submit():
        remember_me = form.remember_me.data
        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user, remember=remember_me)
        next = request.form.get('next')
        if next != 'None':
            # print(next)
            return redirect(next)
        return redirect(url_for('basic.logged_in'))

    return render_template("basic/index.html", form=form, email_form=email_form, next=next)


#The home page of logged in users.
#List all the topics created by the logged-in user
@basic.route('/member', methods = ['GET', 'POST'])
@login_required
def logged_in():
    topics = db.session.query(Topic).filter(Topic.create_by == g.user.email).all()
    return render_template('basic/member.html', full_name=full_name, topics=topics, status=status, menu_categories=menu_categories)


#Register a new account
#Validators implemented in basic.forms.py are applied
@basic.route('/register', methods = ['GET', 'POST'])
def register():
    form = JoinForm()
    if form.validate_on_submit():
        flash('Passed validation')
        hash_password = generate_password_hash(form.password.data)
        active_code = generate_active_code()
        temp = User(form.user_id.data, form.email.data, hash_password, form.first_name.data, form.last_name.data, form.department.data, active_code, form.title.data, form.job.data, form.country.data)
        selected_events = request.form.getlist('selected_events')
        if selected_events is not None:
            for e_id in selected_events:
                fullname = form.first_name.data + ' ' + form.last_name.data
                new_attender = EventAttender(e_id, fullname, form.email.data)
                db.session.add(new_attender)
        db.session.add(temp)
        db.session.commit()
        basic_url = 'http://localhost:5000'
        activate_link = basic_url + url_for('basic.activate_user') + '?active_code=' + active_code
        send_email('Event Manager Registration', ADMINS[0], [form.email.data], "Hello just for testing", \
            render_template('basic/email/registration_confirm.html', full_name=temp.full_name, activate_link=activate_link))

        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user)
        return redirect(url_for('basic.index'))
    current_date = datetime.datetime.now().date()
    events = db.session.query(Event).filter(Event.end_date > current_date).all()
    return render_template("basic/register.html", form=form, events=events)


#Send password reset link to the provided email address
@basic.route('/send_activate')
@login_required
def send_activate_link():
    email = g.user.email
    active_code = refresh_active_code(email)
    basic_url = 'http://localhost:5000'
    activate_link = basic_url + url_for('basic.activate_user') + '?active_code=' + active_code
    send_email('Account activate Link', ADMINS[0], [g.user.email], "", render_template('basic/email/activate_user.html', full_name=full_name, activate_link=activate_link))
    return redirect(url_for('basic.index'))


#Activate user's account and then redirect to the result page.
#Activation is based on the activation code provied in the link in activation email
#ATTENTION: email template has not been implemented yet.
#Testing is based on manual inputing the URL
@basic.route('/activate_user')
@login_required
def activate_user():
    user_id = g.user.user_id
    # menus = menus_of_role()
    active_code = request.args.get("active_code")
    fetched_user = db.session.query(User).filter(User.active_code == active_code).first()
    if fetched_user != None:
        fetched_user_id = fetched_user.user_id
    else:
        fetched_user_id = '0'
    result = 'Succeeded'
    if user_id == fetched_user_id:
        if fetched_user.status != 0:
            msg = 'You account has already been activated.'
        else:
            fetched_user.status = 1
            db.session.commit()
            g.user = fetched_user
            msg = 'Thank you. Your account has been activated successfully.'
        new_active_code = refresh_active_code(fetched_user.email)
        
    else:
        msg = "Sorry, your activation code is invalid. Please try again."
        result = 'Failed'
    return render_template('basic/activate_result.html', msg=msg, result=result, full_name= full_name, status=status, menu_categories=menu_categories)


#Logout user
@basic.route('/logout')
def logout():
    if g.user is not None and g.user.is_authenticated:
        logout_user()
    return redirect(url_for("basic.index"))


#Send password reset link to the provided email address
@basic.route('/send_pwd_reset', methods=['GET', 'POST'])
def send_password_reset_link():
    form = RetrievePwdForm()
    basic_url = 'http://localhost:5000'
    if form.validate_on_submit():
        locked_user = db.session.query(User).filter(User.email == form.email.data).first()
        active_code = refresh_active_code(locked_user.email)
        full_name = locked_user.full_name
        last_name = locked_user.last_name
        name = str(full_name+" "+last_name)
        reset_link = basic_url + url_for('basic.password_reset') + '?email=' + form.email.data + '&active_code=' + active_code
        send_email('Password Reset Link', ADMINS[0], [form.email.data], "", render_template('basic/email/forgot_password.html', name=name, reset_link=reset_link))
    else:
        flash("Invalid Email Address")
    return redirect(url_for('basic.index'))


#Used to reset user's password.
#This page is reached by the password-reset link in the email.
#The authentication is based on the email address and active code in the link URL.
@basic.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    form = PwdResetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_id = request.form.get('user_id')
            hash_password = generate_password_hash(form.password.data) 
            temp = db.session.query(User).filter(User.user_id==user_id).first()
            temp.password = hash_password
            new_active_code = refresh_active_code(temp.email)
            db.session.commit()
            return redirect(url_for('basic.index'))

        else:
            flash("Two passwords must match")
            active_code = request.form.get('active_code')
            email = request.form.get('email')
            auth_info = '?email='+email+'&active_code='+active_code
            return redirect(url_for("basic.password_reset") + auth_info)
    
    active_code = request.args.get('active_code')
    email = request.args.get('email')
    fetched_user = db.session.query(User).filter(User.email == email).first()
    error_msg = ""
    user_id = ""
    if fetched_user == None:
        error_msg = 'Invalid Email Address.'
    else:
        #print(fetched_user.active_code)
        if fetched_user.active_code != active_code:
            error_msg = 'Invalid Active Code.'
        else:
            user_id = fetched_user.user_id

    return render_template('basic/reset_pwd.html', user_id=user_id, error_msg=error_msg, form=form, email=email, active_code=active_code)


#Get terms from autocomplete and return user sets back to create_topic.html.
#Terms can be a part of full name or user id.
@basic.route('/ajax_speaker')
def ajax_speaker():
    term = request.args.get("term", None)
    user_fullname = User.query.filter(User.full_name.contains(term)).all()
    user_userId = User.query.filter(User.user_id.contains(term)).all()
    speakers = set(user_fullname).union(set(user_userId))
    speaker_list = list()
    for speaker in speakers:
        single_record = {'label': speaker.full_name, 'value': speaker.user_id}
        speaker_list.append(single_record)
    # print (speaker_list)
    return json.dumps(speaker_list)
    
    
#Only used for generate initial database
@basic.route('/generate_db')
def generate_db():
    normal_role = Role('normal', 'NM', 'default role for testing', 'i325390')
    admin_role = Role('admin', 'AD', 'default role for testing ADMIN', 'i325390')
    presenter_role = Role('Presenter', 'PS', 'presenter is presenter', 'i325391')
    demostaff_role = Role('Demo Staff', 'DS', 'Demo Staff is Demo Staff', 'i325391')

    em_menu1 = Menu('Place Topics','PT', 'Event Management', 'EM',  '/topic/place', 'i325390')
    em_menu2 = Menu('Validate Topics','VT', 'Event Management', 'EM',  '/topic/validate', 'i325390')
    em_menu3 = Menu('Arrange Topics','AT', 'Event Management', 'EM',  '/topic/arrange', 'i325390')

    mm_menu1 = Menu('Menus and Roles', 'MRI', 'Menu Management', 'MM', '/dataConfig/menus_and_roles', 'i325390')
    mm_menu2 = Menu('Add Menus', 'AM', 'Menu Management', 'MM', '/dataConfig/create_menu', 'i325390')

    # rm_menu = Menu('Role Management', 'RM',  'Menu/Role Management', 'i325390')
    normal_em1 = Role_menu('NM', 'VT', 'i325390')
    normal_em2 = Role_menu('NM', 'PT', 'i325390')
    normal_em3 = Role_menu('NM', 'AT', 'i325390')
    normal_mm1 = Role_menu('NM', 'MRI', 'i325390')
    normal_mm2 = Role_menu('NM', 'AM', 'i325390')

    admin_em1 = Role_menu('AD', 'PT', 'i325390')
    admin_em2 = Role_menu('AD', 'AT', 'i325390')
    admin_em3 = Role_menu('AD', 'VT', 'i325390')
    admin_mm1 = Role_menu('AD', 'MRI', 'i325390')
    admin_mm2 = Role_menu('AD', 'AM', 'i325390')

    presenter_em1 = Role_menu('PS', 'VT', 'i325391')
    presenter_em2 = Role_menu('PS', 'PT', 'i325391')
    presenter_em3 = Role_menu('PS', 'AT', 'i325391')
    presenter_mm1 = Role_menu('PS', 'MRI', 'i325390')
    presenter_mm2 = Role_menu('PS', 'AM', 'i325390')

    demostaff_em1 = Role_menu('DS', 'VT', 'i325391')
    demostaff_em2 = Role_menu('DS', 'PT', 'i325391')
    demostaff_em3 = Role_menu('DS', 'AT', 'i325391')
    demostaff_mm1 = Role_menu('DS', 'MRI', 'i325390')
    demostaff_mm2 = Role_menu('DS', 'AM', 'i325390')

    c_hana = Content('S/4HANA', 'S4HANA', 'i325391')
    c_ue = Content('User Experience', 'UE', 'i325391')
    c_hhci= Content('HANA, HCP & Cloud Infrastructure', 'HHCI', 'i325391')
    c_sme = Content('Small & Medium Enterprises', 'SME', 'i325391')
    c_iot = Content('Internet of Things', 'IOT', 'i325391')
    c_other = Content('Other', 'Other', 'i325391')
    c_iet = Content('Incubation & Emerging Trends', 'IET', 'i325391')
    c_ana = Content('Analytics', 'ANA', 'i325391')
    c_loba = Content('LoB Applications', 'LOBA', 'i325391')
    c_ina = Content('Industry Applications', 'INA', 'i325391')
    c_see = Content('Security & Engineering Excellence', 'SEE', 'i325391')
    c_bna = Content('Business Network Applications', 'BNA', 'i325391')

    f_db = Format('Downtown Block', 'i325390', 'DB')
    f_st = Format('SAP Talk', 'i325390', 'ST')
    f_iz = Format('Interactive Zone', 'i325390', 'IZ')
    f_dfb = Format('Developer Faire Booth', 'i325390', 'DFB')
    rt_sf = ResourceType('Show Floor', 'i325390')
    rt_sb = ResourceType('Small Ballroom', 'i325390')
    rt_lb = ResourceType('Large Ballroom', 'i325390')


    db.session.add(normal_role)
    db.session.add(admin_role)
    db.session.add(presenter_role)
    db.session.add(demostaff_role)

    db.session.add(em_menu1)
    db.session.add(em_menu2)
    db.session.add(em_menu3)
    db.session.add(mm_menu1)
    db.session.add(mm_menu2)

    db.session.add(normal_em1)
    db.session.add(normal_em2)
    db.session.add(normal_em3)
    db.session.add(normal_mm1)
    db.session.add(normal_mm2)

    db.session.add(admin_em1)
    db.session.add(admin_em2)
    db.session.add(admin_em3)
    db.session.add(admin_mm1)
    db.session.add(admin_mm2)

    db.session.add(presenter_em1)
    db.session.add(presenter_em2)
    db.session.add(presenter_em3)
    db.session.add(presenter_mm1)
    db.session.add(presenter_mm2)

    db.session.add(demostaff_em1)
    db.session.add(demostaff_em2)
    db.session.add(demostaff_em3)
    db.session.add(demostaff_mm1)
    db.session.add(demostaff_mm2)

    db.session.add(c_hana)
    db.session.add(c_ue)
    db.session.add(c_hhci)
    db.session.add(c_sme)
    db.session.add(c_iot)
    db.session.add(c_other)
    db.session.add(c_iet)
    db.session.add(c_ana)
    db.session.add(c_loba)
    db.session.add(c_ina)
    db.session.add(c_see)
    db.session.add(c_bna)

    db.session.add(f_db)
    db.session.add(f_st)
    db.session.add(f_dfb)
    db.session.add(f_iz)
    db.session.add(rt_sf)
    db.session.add(rt_sb)
    db.session.add(rt_lb)
    db.session.commit()

    user = User('i325390', '85230316@qq.com', generate_password_hash('12345'), 'Feiyang', \
        'Ye', 'MD office', generate_active_code(), 'Mr.', 'Intern', 'China', 'Presenter')

    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    
    return redirect(url_for('basic.generate_real_resource'))


#Only used for generating resources.
# @basic.route('/generate_resources')
# @login_required
# def generate_resource():
#     resource1 = Resource('SF_001', 'SF_001', 'Show Floor on the first floor', 20, g.user.user_id, 'Show Floor')
#     resource2 = Resource('SF_002', 'SF_002', 'Show Floor on the second floor', 15, g.user.user_id, 'Show Floor')
#     resource3 = Resource('SF_003', 'SF_003', 'Show Floor on the third floor', 10, g.user.user_id, 'Show Floor')
#     resource4 = Resource('SB_001', 'SB_001', 'Small Ballroom on the first floor', 50, g.user.user_id, 'Small Ballroom')
#     resource5 = Resource('LB_001', 'LB_001', 'large Ballroom on the first floor', 100, g.user.user_id, 'Large Ballroom')

#     db.session.add(resource1)
#     db.session.add(resource2)
#     db.session.add(resource3)
#     db.session.add(resource4)
#     db.session.add(resource5)
#     db.session.commit()

#     return redirect(url_for('basic.index'))


#Only used for generating real resources.
@basic.route('/generate_real_resources')
@login_required
def generate_real_resource():
    rt_st = ResourceType('SAP Talk', 'i325390')
    rt_db = ResourceType('Downtown Block', 'i325390')
    rt_dfb = ResourceType('Developer Faire Booth', 'i325390')
    rt_iz = ResourceType('Interactive Zone', 'i325390')
    db.session.add(rt_st)
    db.session.add(rt_db)
    db.session.add(rt_dfb)
    db.session.add(rt_iz)
    db.session.commit()

    resource1 = Resource('SAP Talk 1', 'ST_01', 'SAP Talk 1', 100, g.user.user_id, 'SAP Talk')
    resource2 = Resource('SAP Talk 2', 'ST_02', 'SAP Talk 2', 100, g.user.user_id, 'SAP Talk')
    resource3 = Resource('SAP Talk 3', 'ST_03', 'SAP Talk 3', 100, g.user.user_id, 'SAP Talk')
    resource4 = Resource('Downtown Block 1', 'DB_01', 'Downtown Block 1', 100, g.user.user_id, 'Downtown Block')
    resource5 = Resource('Downtown Block 2', 'DB_02', 'Downtown Block 2', 100, g.user.user_id, 'Downtown Block')
    resource6 = Resource('Downtown Block 3', 'DB_03', 'Downtown Block 3', 100, g.user.user_id, 'Downtown Block')
    resource7 = Resource('Downtown Block 4', 'DB_04', 'Downtown Block 4', 100, g.user.user_id, 'Downtown Block')
    resource8 = Resource('Downtown Block 5', 'DB_05', 'Downtown Block 5', 100, g.user.user_id, 'Downtown Block')
    resource9 = Resource('Downtown Block 6', 'DB_06', 'Downtown Block 6', 100, g.user.user_id, 'Downtown Block')
    resource10 = Resource('Dev. Faire Booth 1', 'DFB_01', 'Developer Faire Booth 1', 100, g.user.user_id, 'Developer Faire Booth')
    resource11 = Resource('Dev. Faire Booth 2', 'DFB_02', 'Developer Faire Booth 2', 100, g.user.user_id, 'Developer Faire Booth')
    resource12 = Resource('Dev. Faire Booth 3', 'DFB_03', 'Developer Faire Booth 3', 100, g.user.user_id, 'Developer Faire Booth')
    resource13 = Resource('Dev. Faire Booth 4', 'DFB_04', 'Developer Faire Booth 4', 100, g.user.user_id, 'Developer Faire Booth')
    resource14 = Resource('Dev. Faire Booth 5', 'DFB_05', 'Developer Faire Booth 5', 100, g.user.user_id, 'Developer Faire Booth')
    resource15 = Resource('Dev. Faire Booth 6', 'DFB_06', 'Developer Faire Booth 6', 100, g.user.user_id, 'Developer Faire Booth')
    resource16 = Resource('Dev. Faire Booth 7', 'DFB_07', 'Developer Faire Booth 7', 100, g.user.user_id, 'Developer Faire Booth')
    resource17 = Resource('Dev. Faire Booth 8', 'DFB_08', 'Developer Faire Booth 8', 100, g.user.user_id, 'Developer Faire Booth')
    resource18 = Resource('Interactive Zone 1', 'IZ_01', 'Interactive Zone 1', 100, g.user.user_id, 'Interactive Zone')
    resource19 = Resource('Interactive Zone 2', 'IZ_02', 'Interactive Zone 2', 100, g.user.user_id, 'Interactive Zone')
    resource20 = Resource('Interactive Zone 3', 'IZ_03', 'Interactive Zone 3', 100, g.user.user_id, 'Interactive Zone')
    resource21 = Resource('Interactive Zone 4', 'IZ_04', 'Interactive Zone 4', 100, g.user.user_id, 'Interactive Zone')

    db.session.add(resource1)
    db.session.add(resource2)
    db.session.add(resource3)
    db.session.add(resource4)
    db.session.add(resource5)
    db.session.add(resource6)
    db.session.add(resource7)
    db.session.add(resource8)
    db.session.add(resource9)
    db.session.add(resource10)
    db.session.add(resource11)
    db.session.add(resource12)
    db.session.add(resource13)
    db.session.add(resource14)
    db.session.add(resource15)
    db.session.add(resource16)
    db.session.add(resource17)
    db.session.add(resource18)
    db.session.add(resource19)
    db.session.add(resource20)
    db.session.add(resource21)
    db.session.commit()

    return redirect(url_for('basic.generate_events'))


#Only used for generating events.
@basic.route('/generate_events')
@login_required
def generate_events():
    e1_from = datetime.datetime.strptime('2016-01-15', '%Y-%m-%d')
    e1_to = datetime.datetime.strptime('2016-01-18', '%Y-%m-%d')
    e2_from = datetime.datetime.strptime('2016-01-25', '%Y-%m-%d')
    e2_to = datetime.datetime.strptime('2016-01-28', '%Y-%m-%d')
    e3_from = datetime.datetime.strptime('2016-01-19', '%Y-%m-%d')
    e3_to = datetime.datetime.strptime('2016-01-21', '%Y-%m-%d')
    event1 = Event('12345', 'dkom', 'Developer kick-off meeting', e1_from, e1_to, 'Emails/dkom/dkom.html', g.user.user_id)
    event2 = Event('23456', 'buss-meeting', 'Global business meeting', e2_from, e2_to, 'upload/email/dkom.html', g.user.user_id)
    event3 = Event('34567', 't-build', 'Team building', e3_from, e3_to, 'Emails/t-build/t-build.html', g.user.user_id)
    db.session.add(event1)
    db.session.add(event2)
    db.session.add(event3)
    db.session.commit()
    return redirect(url_for('basic.index'))


#Required by LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Refresh global variable before the request
@basic.before_request
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


#Generate the active code.
#Active code has length of 4, containing upper and lower case of letters only.
def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    return str(active_code)


#Refresh the active code of the given email account and return the new active code
def refresh_active_code(email):
    user = db.session.query(User).filter(User.email == email).first()
    new_active_code = generate_active_code()
    user.active_code = new_active_code
    db.session.commit()
    return new_active_code

