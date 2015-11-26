from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateRoleForm
from ..models import User, Role
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random


role = Blueprint('role', __name__, template_folder='templates')


# Responsible for creating Roles.
@role.route('/create', methods = ['GET', 'POST'])
@login_required
def create_role():
    first_name = g.user.first_name
    last_name = g.user.last_name
    create_by = last_name + ' ' + first_name
    status = g.user.status
    sidebar = "create_role"
    form = CreateRoleForm()
    if form.validate_on_submit():
        temp = Role(form.rolename.data, form.description.data, create_by)
        db.session.add(temp)
        db.session.commit()
        return redirect(url_for('basic.logged_in'))
    return render_template("create_role.html", form=form, first_name=first_name, sidebar=sidebar, status=status)

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
    return redirect(url_for("basic.index"))

#Render to the events modification page.
#If method is GET, show the event info on the form for the user to modify
#If method is POST, do the validation and update the event 
#ATTENTION: The validation is not working currently
@role.route('/modify/<role_uuid>', methods = ['GET', 'POST'])
@login_required
def modify_role(role_uuid):
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'personal'
    form = CreateEventForm()
    role = Event.query.get(role_uuid)
    if request.method == 'POST':
        print("POST received")
        if form.validate_on_submit():
            #event_id = request.form.get('event_id')
            event.topic = form.topic.data
            event.description = form.description.data
            print (form.start_date.data == None)
            print (form.start_date.data == '')
            event.min_attendance = form.min_attendance.data
            event.max_attendance = form.max_attendance.data
            event.location = form.location.data
            event.host = form.host.data
            event.start_date = form.start_date.data
            event.duration = form.duration.data
            db.session.commit()
            return redirect(url_for("basic.index"))
        else:
            print ("Not validated") 
            return render_template("modify_role.html", form=form, sidebar=sidebar, first_name=first_name, status=status, event_id=event_id)

    if event.is_created_by(g.user.uuid):
        form.topic.data = event.topic
        form.description.data = event.description
        form.location.data = event.location
        form.min_attendance.data = event.min_attendance
        form.max_attendance.data = event.max_attendance
        form.host.data = event.host
        form.duration.data = event.duration
        form.start_date.data = event.start_date
        return render_template("modify_role.html", form=form, sidebar=sidebar, first_name=first_name, status=status, event_id=event_id)
    return redirect(url_for("basic.index"))


#Show all the available events in the website.
#Once finished, should only show approved events
@role.route('/manage')
@login_required
def manage_roles():
    first_name = g.user.first_name
    status = g.user.status
    sidebar = 'public'
    roles = db.session.query(Role).all()


    return render_template('manage_roles.html', roles=roles, first_name=first_name, status=status, sidebar=sidebar)


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Refresh the global variable before every request
@role.before_request
def before_request():
    g.user = current_user