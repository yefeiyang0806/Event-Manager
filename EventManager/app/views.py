from app import app, db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import LoginForm, JoinForm, CreateEventForm
from .models import User, Event
from .emails import send_email
from werkzeug.security import generate_password_hash
import random

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('logged_in'))

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for email = ' + form.email.data)
        remember_me = form.remember_me.data
        temp_user = db.session.query(User).filter(User.email == form.email.data)[0]
        login_user(temp_user, remember=remember_me)

        next = request.args.get('next')
        return redirect(next or url_for('logged_in'))

    return render_template("index.html", form=form)


@app.route('/member', methods = ['GET', 'POST'])
@login_required
def logged_in():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'personal'
    events = g.user.events.all()
    # print(events)
    return render_template('member.html', first_name=first_name, events=events, sidebar=sidebar, status=status)


@app.route('/register', methods = ['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/activate_user')
@login_required
def activate_user():
    first_name = g.user.first_name
    user_uuid = g.user.uuid
    active_code = request.args.get("active_code")
    fetched_user = db.session.query(User).filter(User.active_code == active_code).first()
    fetched_uuid = fetched_user.uuid
    result = 'Succeeded'
    if fetched_user.status != 0:
        msg = 'You account has already been activated.'
    elif user_uuid == fetched_uuid:
        fetched_user.status = 1
        db.session.commit()
        msg = 'Thank you. Your account has been activated successfully.'
    else:
        msg = "Sorry, your activation code is invalid. Please try again. You can receive a new activation code by the following link."
        result = 'Failed'
    return render_template('activate_result.html', msg=msg, result=result, first_name= first_name)



@app.route('/create_event', methods = ['GET', 'POST'])
@login_required
def create_event():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = "create_event"
    user_uuid = g.user.uuid
    form = CreateEventForm()
    if form.validate_on_submit():
        flash("Event Validated")
        temp = Event(form.topic.data, form.description.data, form.min_attendance.data, form.max_attendance.data, form.location.data, form.host.data, form.start_date.data, form.duration.data, user_uuid)
        db.session.add(temp)
        db.session.commit()
        return redirect(url_for('logged_in'))
    return render_template("create_event.html", form=form, first_name=first_name, sidebar=sidebar, status=status)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login')
def login():
    first_name = g.user.first_name
    send_email('test subject', ADMINS[0], ['85230316@qq.com'], "Hello just for testing", render_template('email/registration_confirm.html', first_name=first_name))
    return render_template('member.html', first_name='test', status=0)


@app.route('/delete_event')
@login_required
def delete_event():
    event_id = request.args.get('event_id')
    event = db.session.query(Event).filter(Event.id == event_id).first()
    if event.is_created_by(g.user.uuid):
        print ("delete!!!")
        print ("ready to remove the event!")
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for("index"))


@app.route('/modify_event', methods = ['GET', 'POST'])
@login_required
def modify_event():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'personal'
    if request.method == 'POST':
        #modified_event = Event(request.form.get('topic'), request.form.get('description'), 
            #request.form.get('min_attendance'), request.form.get('max_attendance'), request.form.get('location'), 
            #request.form.get('host'), request.form.get('start_date'), request.form.get('duration'), g.user.uuid)
        #db.session.query(Event).filter(Event.id == event.id).first().update()
        event_id = request.form.get('event_id')
        event = Event.query.get(event_id)
        event.topic = request.form.get('topic')
        event.description = request.form.get('description')
        event.min_attendance = request.form.get('min_attendance')
        event.max_attendance = request.form.get('max_attendance')
        event.location = request.form.get('location')
        event.host = request.form.get('host')
        event.start_date = request.form.get('start_date')
        event.duration = request.form.get('duration')
        db.session.commit()
        return redirect(url_for("index"))

    event_id = request.args.get('event_id')
    event = Event.query.get(event_id)
    if event.is_created_by(g.user.uuid):
        form = CreateEventForm()
        form.topic.data = event.topic
        form.description.data = event.description
        form.location.data = event.location
        form.min_attendance.data = event.min_attendance
        form.max_attendance.data = event.max_attendance
        form.host.data = event.host
        form.duration.data = event.duration
        form.start_date.data = event.start_date
        return render_template("modify_event.html", form=form, sidebar=sidebar, first_name=first_name, status=status, event_id=event_id)
    return redirect(url_for("index"))


@app.route('/view_event')
@login_required
def view_event():
    first_name = g.user.first_name
    status = g.user.status
    event_id = request.args.get('id')
    event = db.session.query(Event).filter(Event.id == event_id).first()
    if event.is_created_by(g.user.uuid):
        sidebar = 'personal'
        mode = 'creator'
    else:
        sidebar = 'public'
        mode = 'viewer'
    return render_template('view_event.html', event=event, mode=mode, first_name=first_name, status=status, sidebar=sidebar)


@app.route('/available_events')
@login_required
def available_events():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'public'
    events = db.session.query(Event).all()
    return render_template('available_events.html', events=events, first_name=first_name, status=status, sidebar=sidebar)


@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


@app.before_request
def before_request():
    g.user = current_user


def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    print ("active code: " + active_code)
    return active_code