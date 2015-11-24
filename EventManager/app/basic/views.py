from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import LoginForm, JoinForm
from ..models import User, Event
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


basic = Blueprint('basic', __name__, template_folder='templates')

@basic.route('/')
@basic.route('/index', methods = ['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('basic.logged_in'))

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for email = ' + form.email.data)
        remember_me = form.remember_me.data
        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user, remember=remember_me)

        next = request.args.get('next')
        return redirect(next or url_for('basic.logged_in'))

    return render_template("index.html", form=form)


@basic.route('/member', methods = ['GET', 'POST'])
@login_required
def logged_in():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'personal'
    events = g.user.events.all()
    # print(events)
    return render_template('member.html', first_name=first_name, events=events, sidebar=sidebar, status=status)


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
        send_email('Event Manager Registration', ADMINS[0], [form.email.data], "Hello just for testing", render_template('email/registration_confirm.html', first_name=form.first_name.data))

        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user)
        return redirect(url_for('basic.index'))
    return render_template("register.html", form=form)


@basic.route('/activate_user')
@login_required
def activate_user():
    first_name = g.user.first_name
    user_uuid = g.user.uuid
    active_code = request.args.get("active_code")
    fetched_user = db.session.query(User).filter(User.active_code == active_code).first()
    fetched_uuid = fetched_user.uuid
    result = 'Succeeded'
    if user_uuid == fetched_uuid:
        if fetched_user.status != 0:
            msg = 'You account has already been activated.'
        else:
            fetched_user.status = 1
            db.session.commit()
            g.user = fetched_user
            msg = 'Thank you. Your account has been activated successfully.'
    else:
        msg = "Sorry, your activation code is invalid. Please try again. You can receive a new activation code by the following link."
        result = 'Failed'
    status = g.user.status
    return render_template('activate_result.html', msg=msg, result=result, first_name= first_name, status=status)


@basic.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("basic.index"))


@basic.route('/login')
def login():
    first_name = g.user.first_name
    send_email('test subject', ADMINS[0], ['85230316@qq.com'], "Hello just for testing", render_template('email/registration_confirm.html', first_name=first_name))
    return render_template('member.html', first_name='test', status=0)


@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


@basic.before_request
def before_request():
    g.user = current_user


def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    print ("active code: " + active_code)
    return active_code