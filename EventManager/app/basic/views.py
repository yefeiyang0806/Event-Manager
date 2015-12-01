from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import LoginForm, JoinForm, RetrievePwdForm, PwdResetForm
from ..models import User, Event, Menu, Role, Role_menu
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


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
    if form.validate_on_submit():
        flash('Login requested for email = ' + form.email.data)
        remember_me = form.remember_me.data
        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user, remember=remember_me)
        next = request.args.get('next')
        return redirect(next or url_for('basic.logged_in'))

    return render_template("basic/index.html", form=form, email_form=email_form)


#The home page of logged in users.
#List all the events created by the logged-in user
@basic.route('/member', methods = ['GET', 'POST'])
@login_required
def logged_in():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'personal'
    events = g.user.events.all()
    menus = menus_of_role()
    # print(events)
    return render_template('basic/member.html', first_name=first_name, events=events, status=status, menus=menus)


#Register a new account
#Validators implemented in basic.forms.py are applied
@basic.route('/register', methods = ['GET', 'POST'])
def register():
    form = JoinForm()
    if form.validate_on_submit():
        flash('Passed validation')
        hash_password = generate_password_hash(form.password.data)
        active_code = generate_active_code()
        temp = User(form.email.data, hash_password, form.first_name.data, form.last_name.data, active_code)
        db.session.add(temp)
        db.session.commit()
        basic_url = 'http://localhost:5000'
        activate_link = basic_url + url_for('basic.activate_user') + '?active_code=' + active_code
        send_email('Event Manager Registration', ADMINS[0], [form.email.data], "Hello just for testing", \
            render_template('basic/email/registration_confirm.html', first_name=form.first_name.data, activate_link=activate_link))

        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user)
        return redirect(url_for('basic.index'))
    return render_template("basic/register.html", form=form)


#Send password reset link to the provided email address
@basic.route('/send_activate')
@login_required
def send_activate_link():
    first_name = g.user.first_name
    email = g.user.email
    active_code = refresh_active_code(email)
    basic_url = 'http://localhost:5000'
    activate_link = basic_url + url_for('basic.activate_user') + '?active_code=' + active_code
    send_email('Account activate Link', ADMINS[0], [g.user.email], "", render_template('basic/email/activate_user.html', first_name=first_name, activate_link=activate_link))
    return redirect(url_for('basic.index'))


#Activate user's account and then redirect to the result page.
#Activation is based on the activation code provied in the link in activation email
#ATTENTION: email template has not been implemented yet.
#Testing is based on manual inputing the URL
@basic.route('/activate_user')
@login_required
def activate_user():
    first_name = g.user.first_name
    user_uuid = g.user.uuid
    menus = menus_of_role()
    active_code = request.args.get("active_code")
    fetched_user = db.session.query(User).filter(User.active_code == active_code).first()
    if fetched_user != None:
        fetched_uuid = fetched_user.uuid
    else:
        fetched_uuid = '0'
    result = 'Succeeded'
    if user_uuid == fetched_uuid:
        if fetched_user.status != 0:
            msg = 'You account has already been activated.'
        else:
            fetched_user.status = 1
            db.session.commit()
            g.user = fetched_user
            msg = 'Thank you. Your account has been activated successfully.'
        new_active_code = refresh_active_code(fetched_user.email)
        
    else:
        msg = "Sorry, your activation code is invalid. Please try again. You can receive a new activation code by the following link."
        result = 'Failed'
    status = g.user.status
    return render_template('basic/activate_result.html', msg=msg, result=result, first_name= first_name, status=status, menus=menus)


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
        first_name = locked_user.first_name
        last_name = locked_user.last_name
        name = str(first_name+" "+last_name)
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
            uuid = request.form.get('uuid')
            hash_password = generate_password_hash(form.password.data) 
            temp = db.session.query(User).get(uuid)
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
    uuid = ""
    if fetched_user == None:
        error_msg = 'Invalid Active Code.'
    else:
        print(fetched_user.active_code)
        if fetched_user.active_code != active_code:
            error_msg = 'Invalid Active Code.'
        else:
            uuid = fetched_user.uuid

    return render_template('basic/reset_pwd.html', uuid=uuid, error_msg=error_msg, form=form, email=email, active_code=active_code)


#Only for testing purpose
#Test the feature of sending emails
@basic.route('/login')
def login():
    #first_name = g.user.first_name
    send_email('test subject', ADMINS[0], ['85230316@qq.com'], "Hello just for testing", render_template('email/registration_confirm.html', first_name=first_name))
    return render_template('basic/member.html', first_name='test', status=0)


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
        menu = db.session.query(Menu).get(m.menu_id)
        menus.append(menu)
    print (menus)
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

#
@basic.upload('/upload_file', methods=['GET', 'POST'])
def upload_file():
    UPLOAD_FOLDER = '/path/to/the/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    form = PwdResetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            uuid = request.form.get('uuid')
            hash_password = generate_password_hash(form.password.data) 
            temp = db.session.query(User).get(uuid)
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
    uuid = ""
    if fetched_user == None:
        error_msg = 'Invalid Active Code.'
    else:
        print(fetched_user.active_code)
        if fetched_user.active_code != active_code:
            error_msg = 'Invalid Active Code.'
        else:
            uuid = fetched_user.uuid

    return render_template('basic/reset_pwd.html', uuid=uuid, error_msg=error_msg, form=form, email=email, active_code=active_code)