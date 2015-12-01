from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateEventForm
from ..models import User, Event, Role, Menu, Role_menu, Content, Format
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


event = Blueprint('event', __name__)


# Responsible for creating events.
@event.route('/create', methods = ['GET', 'POST'])
@login_required
def create_event():
    first_name = g.user.first_name
    status = g.user.status
    user_uuid = g.user.uuid
    menus = menus_of_role()
    form = CreateEventForm()
    form.set_options()
    if form.validate_on_submit():
        #print (db.session.query(Content).filter(Content.name == form.content.data).first().events.count())
        temp = Event(form.topic.data, form.description.data, form.min_attendance.data, form.max_attendance.data, form.speaker.data, user_uuid, form.content.data, form.format.data)
        db.session.add(temp)
        db.session.commit()
        #print (db.session.query(Content).filter(Content.name == form.content.data).first().events.count())
        return redirect(url_for('basic.logged_in'))
    return render_template("event/create_event.html", form=form, first_name=first_name, status=status, menus=menus)


#Responsible for deleting existing events.
#Called by jquery in event.view_event.html and basic.member.html
@event.route('/delete')
@login_required
def delete_event():
    event_uuid = request.args.get('event_uuid')
    event = db.session.query(Event).filter(Event.uuid == event_uuid).first()
    if event.is_created_by(g.user.uuid):
        print ("delete!!!")
        print ("ready to remove the event!")
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for("basic.index"))


#Render to the events modification page.
#If method is GET, show the event info on the form for the user to modify
#If method is POST, do the validation and update the event 
#ATTENTION: The validation is not working currently
@event.route('/modify/<event_uuid>', methods = ['GET', 'POST'])
@login_required
def modify_event(event_uuid):
    first_name = g.user.first_name
    status = g.user.status
    form = CreateEventForm()
    form.set_options()
    event = Event.query.get(event_uuid)
    if request.method == 'POST':
        print("POST received")
        if form.validate_on_submit():
            #event_id = request.form.get('event_id')
            event.topic = form.topic.data
            event.description = form.description.data
            event.min_attendance = form.min_attendance.data
            event.max_attendance = form.max_attendance.data
            event.speaker = form.speaker.data
            event.format = form.format.data
            event.content = form.content.data
            db.session.commit()
            return redirect(url_for("basic.index"))
        else:
            print ("Not validated")
            menus = menus_of_role()
            return render_template("event/modify_event.html", form=form,\
                first_name=first_name, status=status, event_uuid=event_uuid, menus=menus)

    if event.is_created_by(g.user.uuid):
        form.topic.data = event.topic
        form.description.data = event.description
        form.min_attendance.data = event.min_attendance
        form.max_attendance.data = event.max_attendance
        form.speaker.data = event.speaker
        form.content.data = event.content
        form.format.data = event.format
        menus = menus_of_role()
        return render_template("event/modify_event.html", form=form,\
            first_name=first_name, status=status, event_uuid=event_uuid, menus=menus)
    return redirect(url_for("basic.index"))



#Reached by the link on the events' topics. Show details of the selected event
@event.route('/view')
@login_required
def view_event():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    event_uuid = request.args.get('uuid')
    print (event_uuid)
    print("-----------------------------")
    event = db.session.query(Event).filter(Event.uuid == event_uuid).first()
    if event.is_created_by(g.user.uuid):
        mode = 'creator'
    else:
        mode = 'viewer'
    return render_template('event/view_event.html', event=event, mode=mode, first_name=first_name,\
        status=status, menus=menus)


#Show all the available events in the website.
#Once finished, should only show approved events
@event.route('/available')
@login_required
def available_events():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    events = db.session.query(Event).all()
    return render_template('event/available_events.html', events=events, first_name=first_name, status=status, menus=menus)


#Show the page of scheduling all the approved events. The page is reached by the "Arrange Event link in the event management side bar"
@event.route('/arrange')
@login_required
def arrange_events():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    contents = db.session.query(Content).all()
    formats = db.session.query(Format.name).all()
    content_names = list()
    format_names = list()
    for c in contents:
        content_names.append(str(c.name))
    for f in formats:
        format_names.append(str(f.name))

    print(content_names)

    if content_filter != None and format_filter != None:
        events_content = db.session.query(Content).filter(Content.name == content_filter).first().events.all()
        events_format = db.session.query(Format).filter(Format.name == format_filter).first().events.all()
        events = set(events_format).intersection(events_content)
    elif content_filter != None and format_filter == None:
        events = db.session.query(Content).filter(Content.name == content_filter).first().events.all()
    elif content_filter == None and format_filter != None:
        events = db.session.query(Format).filter(Format.name == format_filter).first().events.all()
    else:
        events = db.session.query(Event).all()
    #print (events)
    return render_template('event/arrange_events.html', events=events, first_name=first_name, status=status, \
        menus=menus, content_names=content_names, format_names=format_names)


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).get(m.menu_id)
        menus.append(menu)
    #print (menus)
    return menus


#Refresh the global variable before every request
@event.before_request
def before_request():
    g.user = current_user