from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateTopicForm
from ..models import User, Topic, Role, Menu, Role_menu, Content, Format, ResourceType, Resource
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random
import re


topic = Blueprint('topic', __name__)


# Responsible for creating topics.
@topic.route('/create', methods = ['GET', 'POST'])
@login_required
def create_topic():
    first_name = g.user.first_name
    status = g.user.status
    user_id = g.user.user_id
    menus = menus_of_role()
    form = CreateTopicForm()
    form.set_options()   
    
    if form.validate_on_submit():      
        startdata = form.DateStart.data.split('-')
        year_start = startdata[0]
        month_start = startdata[1]
        day_start = startdata[2]
               #print (db.session.query(Content).filter(Content.name == form.content.data).first().topics.count())
        temp = Topic(form.title.data, form.description.data, form.min_attendance.data, form.max_attendance.data,\
                form.speaker1.data, form.speaker2.data, form.speaker3.data, year_start, month_start, day_start,\
                form.day_duration.data, form.hour_duration.data, form.minute_duration.data, user_id,\
                form.content.data, form.format.data, form.location.data, form.link.data, form.jamlink.data)     
        db.session.add(temp)
        db.session.commit()
        #print (db.session.query(Content).filter(Content.name == form.content.data).first().topics.count())user_email, 
        return redirect(url_for('basic.logged_in'))
    return render_template("topic/create_topic.html", form=form, first_name=first_name, status=status, menus=menus)


#Responsible for deleting existing topics.
#Called by jquery in topic.view_topic.html and basic.member.html
@topic.route('/delete')
@login_required
def delete_topic():
    topic_uuid = request.args.get('topic_uuid')
    topic = db.session.query(topic).filter(topic.uuid == topic_uuid).first()
    if topic.is_created_by(g.user.email):
        print ("delete!!!")
        print ("ready to remove the topic!")
        db.session.delete(topic)
        db.session.commit()
    return redirect(url_for("basic.index"))


#Render to the topics modification page.
#If method is GET, show the topic info on the form for the user to modify
#If method is POST, do the validation and update the topic 
#ATTENTION: The validation is not working currently
@topic.route('/modify/<topic_uuid>', methods = ['GET', 'POST'])
@login_required
def modify_topic(topic_uuid):
    first_name = g.user.first_name
    status = g.user.status
    form = CreatetopicForm()
    form.set_options()
    topic = topic.query.get(topic_uuid)
    if request.method == 'POST':
        print("POST received")
        if form.validate_on_submit():
            #topic_id = request.form.get('topic_id')
            topic.title = form.title.data
            topic.short_text = form.short_text.data
            topic.description = form.description.data
            topic.min_attendance = form.min_attendance.data
            topic.max_attendance = form.max_attendance.data
            startdata = form.DateStart.data.split('-')
            topic.year_start = startdata[0]
            topic.month_start = startdata[1]
            topic.day_start = startdata[2]           
            topic.day_duration =  form.day_duration.data
            topic.hour_duration = form.hour_duration.data 
            topic.minute_duration = form.minute_duration.data
            topic.speaker = form.speaker.data
            topic.format = form.format.data
            topic.content = form.content.data
            db.session.commit()
            return redirect(url_for("basic.index"))
        else:
            print ("Not validated")
            menus = menus_of_role()
            return render_template("topic/modify_topic.html", form=form,\
                first_name=first_name, status=status, topic_uuid=topic_uuid, menus=menus)

    if topic.is_created_by(g.user.email):
        form.title.data = topic.title
        form.short_text.data = topic.short_text
        form.description.data = topic.description
        form.min_attendance.data = topic.min_attendance
        form.max_attendance.data = topic.max_attendance        
        form.DateStart.data = topic.year_start + topic.month_start + topic.day_start
        form.day_duration.data = topic.day_duration
        form.hour_duration.data = topic.hour_duration
        form.minute_duration.data = topic.minute_duration
        form.speaker.data = topic.speaker
        form.content.data = topic.content
        form.format.data = topic.format
        menus = menus_of_role()
        return render_template("topic/modify_topic.html", form=form,\
            first_name=first_name, status=status, topic_uuid=topic_uuid, menus=menus)
    return redirect(url_for("basic.index"))



#Reached by the link on the topics' titles. Show details of the selected topic
@topic.route('/view')
@login_required
def view_topic():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    topic_uuid = request.args.get('uuid')
    topic = db.session.query(topic).filter(topic.uuid == topic_uuid).first()
    if topic.is_created_by(g.user.email):
        mode = 'creator'
    else:
        mode = 'viewer'
    return render_template('topic/view_topic.html', topic=topic, mode=mode, first_name=first_name,\
        status=status, menus=menus)


#Show all the available topics in the website.
#Once finished, should only show approved topics
@topic.route('/available')
@login_required
def available_topics():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    topics = db.session.query(topic).all()
    return render_template('topic/available_topics.html', topics=topics, first_name=first_name, status=status, menus=menus)


#Show the page of scheduling all the approved topics. The page is reached by the "Arrange topic link in the topic management side bar"
@topic.route('/arrange')
@login_required
def arrange_topics():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    contents = db.session.query(Content).all()
    formats = db.session.query(Format).all()
    content_names = list()
    format_names = list()
    for c in contents:
        content_names.append(str(c.name))
    for f in formats:
        format_names.append(str(f.name))

    if content_filter != None and format_filter != None:
        topics_content = db.session.query(Content).filter(Content.name == content_filter).first().topics.all()
        topics_format = db.session.query(Format).filter(Format.name == format_filter).first().topics.all()
        topics = set(topics_format).intersection(topics_content)
    elif content_filter != None and format_filter == None:
        topics = db.session.query(Content).filter(Content.name == content_filter).first().topics.all()
    elif content_filter == None and format_filter != None:
        topics = db.session.query(Format).filter(Format.name == format_filter).first().topics.all()
    else:
        topics = db.session.query(topic).all()
    #print (topics)
    return render_template('topic/arrange_topics.html', topics=topics, first_name=first_name, status=status, \
        menus=menus, content_names=content_names, format_names=format_names)


#Show the page of scheduling all the approved topics. The page is reached by the "Place topic link in the topic management side bar"
@topic.route('/place')
@login_required
def place_topics():
    first_name = g.user.first_name
    status = g.user.status
    menus = menus_of_role()
    r_type_filter = request.args.get('r_type', None)
    resource_filter = request.args.get('resource', None)
    r_types = db.session.query(ResourceType).all()
    resources = db.session.query(Resource).all()
    r_type_names = list()
    resource_names = list()
    for t in r_types:
        r_type_names.append(str(t.name))
    for r in resources:
        resource_names.append(str(r.name))
    return render_template('topic/place_topics.html', first_name=first_name, status=status, \
        menus=menus, r_type_names=r_type_names, resource_names=resource_names)


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


#Return the corresponding menus of a certain user's role
def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menus.append(menu)
    #print (menus)
    return menus


#Refresh the global variable before every request
@topic.before_request
def before_request():
    g.user = current_user