from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import LoginForm, JoinForm, RetrievePwdForm, PwdResetForm
from ..models import User, Topic, Menu, Role, Role_menu, Content, Format, ResourceType, Resource
from ..emails import send_email
from werkzeug.security import generate_password_hash


import random, json


basic = Blueprint('basic', __name__)


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
            print(next)
            return redirect(next)
        return redirect(url_for('basic.logged_in'))

    return render_template("basic/index.html", form=form, email_form=email_form, next=next)


#The home page of logged in users.
#List all the topics created by the logged-in user
@basic.route('/member', methods = ['GET', 'POST'])
@login_required
def logged_in():
    full_name = g.user.full_name
    status = g.user.status
    topics = db.session.query(Topic).filter(Topic.create_by == g.user.email).all()
    menus = menus_of_role()
    return render_template('basic/member.html', full_name=full_name, topics=topics, status=status, menus=menus)


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
        db.session.add(temp)
        db.session.commit()
        basic_url = 'http://localhost:5000'
        activate_link = basic_url + url_for('basic.activate_user') + '?active_code=' + active_code
        send_email('Event Manager Registration', ADMINS[0], [form.email.data], "Hello just for testing", \
            render_template('basic/email/registration_confirm.html', full_name=temp.full_name, activate_link=activate_link))

        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user)
        return redirect(url_for('basic.index'))
    return render_template("basic/register.html", form=form)


#Send password reset link to the provided email address
@basic.route('/send_activate')
@login_required
def send_activate_link():
    full_name = g.user.full_name
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
    full_name = g.user.full_name
    user_id = g.user.user_id
    menus = menus_of_role()
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
    status = g.user.status
    return render_template('basic/activate_result.html', msg=msg, result=result, full_name= full_name, status=status, menus=menus)


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
    print (speaker_list)
    return json.dumps(speaker_list)
    
    
#Only used for generate initial database
@basic.route('/generate_db')
def generate_db():
    normal_role = Role('normal', 'NM', 'default role for testing', 'i325390')
    admin_role = Role('admin', 'AD', 'default role for testing ADMIN', 'i325390')
    presenter_role = Role('Presenter', 'PS', 'presenter is presenter', 'i325391')
    demostaff_role = Role('Demo Staff', 'DS', 'Demo Staff is Demo Staff', 'i325391')

    em_menu = Menu('Event Management', 'EM',  'Menu/Event Management', 'i325390')
    rm_menu = Menu('Role Management', 'RM',  'Menu/Role Management', 'i325390')
    normal_em = Role_menu('NM', 'EM', 'i325390')
    normal_rm = Role_menu('NM', 'RM', 'i325390')
    admin_em = Role_menu('AD', 'EM', 'i325390')
    admin_rm = Role_menu('AD', 'RM', 'i325390')
    c_hana = Content('HANA', 'HANA', 'i325390')
    c_cloud = Content('Cloud', 'Cloud', 'i325390')
    c_fiori = Content('Fiori', 'Fiori', 'i325390')
    c_abap = Content('ABAP', 'ABAP', 'i325390')
    c_iot = Content('IOT', 'IOT', 'i325390')
    f_df = Format('Developer Fair', 'i325390', 'DF')
    f_db = Format('Downtown Block', 'i325390', 'DB')
    f_st = Format('SAP Talk', 'i325390', 'ST')
    f_ct = Format('Customer Talk', 'i325390', 'CT')
    f_iz = Format('Innovation Zone', 'i325390', 'IZ')
    rt_sf = ResourceType('Show Floor', 'i325390')
    rt_sb = ResourceType('Small Ballroom', 'i325390')
    rt_lb = ResourceType('Large Ballroom', 'i325390')
    
    db.session.add(normal_role)
    db.session.add(admin_role)
    db.session.add(em_menu)
    db.session.add(rm_menu)
    db.session.add(normal_em)
    db.session.add(normal_rm)
    db.session.add(admin_em)
    db.session.add(admin_rm)
    db.session.add(c_hana)
    db.session.add(c_cloud)
    db.session.add(c_fiori)
    db.session.add(c_abap)
    db.session.add(c_iot)
    db.session.add(f_df)
    db.session.add(f_db)
    db.session.add(f_st)
    db.session.add(f_ct)
    db.session.add(f_iz)
    db.session.add(rt_sf)
    db.session.add(rt_sb)
    db.session.add(rt_lb)
    db.session.commit()
    
    return redirect(url_for('basic.index'))


#Only used for generating resources.
@basic.route('/generate_resources')
@login_required
def generate_resource():
    resource1 = Resource('SF_001', 'SF_001', 'Show Floor on the first floor', 20, g.user.user_id, 'Show Floor')
    resource2 = Resource('SF_002', 'SF_002', 'Show Floor on the second floor', 15, g.user.user_id, 'Show Floor')
    resource3 = Resource('SF_003', 'SF_003', 'Show Floor on the third floor', 10, g.user.user_id, 'Show Floor')
    resource4 = Resource('SB_001', 'SB_001', 'Small Ballroom on the first floor', 50, g.user.user_id, 'Small Ballroom')
    resource5 = Resource('LB_001', 'LB_001', 'large Ballroom on the first floor', 100, g.user.user_id, 'Large Ballroom')

    db.session.add(resource1)
    db.session.add(resource2)
    db.session.add(resource3)
    db.session.add(resource4)
    db.session.add(resource5)
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


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menus.append(menu)
    return menus


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

