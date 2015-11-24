from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateEventForm
from ..models import User, Event
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


event = Blueprint('event', __name__, template_folder='templates')


@event.route('/create', methods = ['GET', 'POST'])
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
        return redirect(url_for('basic.logged_in'))
    return render_template("create_event.html", form=form, first_name=first_name, sidebar=sidebar, status=status)


@event.route('/delete')
@login_required
def delete_event():
    event_id = request.args.get('event_id')
    event = db.session.query(Event).filter(Event.id == event_id).first()
    if event.is_created_by(g.user.uuid):
        print ("delete!!!")
        print ("ready to remove the event!")
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for("basic.index"))


@event.route('/modify', methods = ['GET', 'POST'])
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
        return redirect(url_for("basic.index"))

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
    return redirect(url_for("basic.index"))


@event.route('/view')
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


@event.route('/available')
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


@event.before_request
def before_request():
    g.user = current_user