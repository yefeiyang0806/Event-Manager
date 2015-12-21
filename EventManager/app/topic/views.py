# -*- coding: utf-8 -*-
from app import db, lm
from config import ADMINS
from flask import render_template, flash, redirect, session, url_for, request, g, request, Blueprint, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from .forms import CreateTopicForm
from ..models import User, Topic, Role, Menu, Role_menu, Content, Format, ResourceType, Resource, TopicValidation, TopicSchedule
from ..emails import send_email
from werkzeug.security import generate_password_hash
import random, json, datetime
import re


topic = Blueprint('topic', __name__)


# Responsible for creating topics.
@topic.route('/create', methods = ['GET', 'POST'])
@login_required
def create_topic():
    full_name = g.user.full_name
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
        temp = Topic(generate_topic_id(), form.title.data, form.description.data, form.min_attendance.data, form.max_attendance.data,\
                form.speaker1.data, form.speaker2.data, form.speaker3.data, form.speaker4.data, form.speaker5.data, year_start, month_start, day_start,\
                form.day_duration.data, form.hour_duration.data, form.minute_duration.data, g.user.email,\
                form.content.data, form.format.data, form.location.data, form.link.data, form.jamlink.data, form.memo.data)     
        db.session.add(temp)
        db.session.commit()
        #print (db.session.query(Content).filter(Content.name == form.content.data).first().topics.count())user_email, 
        return redirect(url_for('basic.logged_in'))
    return render_template("topic/create_topic.html", form=form, full_name=full_name, status=status, menus=menus)


#Responsible for deleting existing topics.
#Called by jquery in topic.view_topic.html and basic.member.html
@topic.route('/delete')
@login_required
def delete_topic():
    topic_id = request.args.get('topic_id')
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()

    if topic.is_created_by(g.user.email):
        db.session.delete(topic)
        db.session.commit()
    return redirect(url_for("basic.index"))


#Render to the topics modification page.
#If method is GET, show the topic info on the form for the user to modify
#If method is POST, do the validation and update the topic 
#ATTENTION: The validation is not working currently
@topic.route('/modify/<topic_id>', methods = ['GET', 'POST'])
@login_required
def modify_topic(topic_id):
    full_name = g.user.full_name
    status = g.user.status
    form = CreateTopicForm()
    form.set_options()
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    if request.method == 'POST':
        # print("POST received")
        if form.validate_on_submit():
            #topic_id = request.form.get('topic_id')
            topic.title = form.title.data
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
            topic.link = form.link.data
            topic.jamlink = form.jamlink.data
            topic.speaker1 = form.speaker1.data
            topic.speaker2 = form.speaker2.data
            topic.speaker3 = form.speaker3.data
            topic.speaker4 = form.speaker4.data
            topic.speaker5 = form.speaker5.data
            topic.format = form.format.data
            topic.content = form.content.data            
            topic.location = form.location.data
            topic.memo = form.memo.data
            db.session.commit()
            return redirect(url_for("basic.index"))
        else:
            print ("Not validated")
            menus = menus_of_role()
            return render_template("topic/modify_topic.html", form=form,\
                full_name=full_name, status=status, topic_id=topic_id, menus=menus)

    if topic.is_created_by(g.user.email):
        form.title.data = topic.title
        form.description.data = topic.description
        form.min_attendance.data = topic.min_attendance
        form.max_attendance.data = topic.max_attendance        
        form.DateStart.data = topic.year_start + '-'+ topic.month_start +'-' + topic.day_start
        form.day_duration.data = topic.day_duration
        form.hour_duration.data = topic.hour_duration
        form.minute_duration.data = topic.minute_duration

        form.speaker1.data = topic.speaker1
        form.speaker2.data = topic.speaker2
        form.speaker3.data = topic.speaker3
        form.speaker4.data = topic.speaker4
        form.speaker5.data = topic.speaker5
        speaker1_name = User.query.filter(User.user_id == topic.speaker1).first().full_name
        speaker2_name = ''
        speaker3_name = ''
        speaker4_name = ''
        speaker5_name = ''
        if topic.speaker2 != '':
            speaker2_name = User.query.filter(User.user_id == topic.speaker2).first().full_name
        if topic.speaker3 != '':
            speaker3_name = User.query.filter(User.user_id == topic.speaker3).first().full_name
        if topic.speaker4 != '':
            speaker4_name = User.query.filter(User.user_id == topic.speaker4).first().full_name
        if topic.speaker5 != '':
            speaker5_name = User.query.filter(User.user_id == topic.speaker5).first().full_name

        form.content.data = topic.content
        form.format.data = topic.format
        form.link.data = topic.link 
        form.jamlink.data = topic.jamlink 
        form.location.data = topic.location
        menus = menus_of_role()
        return render_template("topic/modify_topic.html", form=form, full_name=full_name, status=status, \
            topic_id=topic_id, menus=menus, speaker1_name=speaker1_name, speaker2_name=speaker2_name, \
            speaker3_name=speaker3_name, speaker4_name=speaker4_name, speaker5_name=speaker5_name)
    return redirect(url_for("basic.index"))



#Reached by the link on the topics' titles. Show details of the selected topic
@topic.route('/view')
@login_required
def view_topic():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    topic_id = request.args.get('topic_id')
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    if topic.is_created_by(g.user.email):
        mode = 'creator'
    else:
        mode = 'viewer'
    return render_template('topic/view_topic.html', topic=topic, mode=mode, full_name=full_name,\
        status=status, menus=menus)


#Show all the available topics in the website.
#Once finished, should only show approved topics
@topic.route('/available')
@login_required
def available_topics():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    topics = db.session.query(Topic).all()
    return render_template('topic/available_topics.html', topics=topics, full_name=full_name, status=status, menus=menus)


#Show the page of scheduling all the approved topics. The page is reached by the "Arrange topic link in the topic management side bar"
@topic.route('/arrange')
@login_required
def arrange_topics():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    results = content_format_location_filter(content_filter, format_filter, location_filter)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    topics = results['topics']
    
    return render_template('topic/arrange_topics.html', topics=topics, full_name=full_name, status=status, \
        menus=menus, content_names=content_names, format_names=format_names, locations=locations)


#Show the page of scheduling all the approved topics. The page is reached by the "Place topic link in the topic management side bar"
@topic.route('/place')
@login_required
def place_topics():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    results = content_format_location_filter(content_filter, format_filter, location_filter)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    return render_template('topic/place_topics.html', full_name=full_name, status=status, \
        menus=menus, content_names=content_names, format_names=format_names, locations=locations)


#Show the page of scheduling all the approved topics. The page is reached by the "validate topic" link in the topic management side bar"
@topic.route('/validate')
@login_required
def validate_topics():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    results = content_format_location_filter(content_filter, format_filter, location_filter)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    topics = results['topics']
    return render_template('topic/validate_topics.html', topics=topics, full_name=full_name, status=status, \
        menus=menus, content_names=content_names, format_names=format_names, locations=locations)
        

# Handle the content sent from the templates to insert validation result into db.
@topic.route('/ajax_validation', methods=["GET", "POST"])
@login_required
def ajax_validation():
    #print(request.get_json(force=True))
    json_data = request.get_json(force=True)
    results = json_data["Results"]
    for result in results:
        topic = db.session.query(Topic).filter(Topic.topic_id == result['topic_id']).first()
        topic_validation = db.session.query(TopicValidation).filter(TopicValidation.topic_title == topic.title).first()
        # print(topic)
        if topic_validation == None:
            topic_validation = TopicValidation(topic.title, topic.year_start, result['validation'], g.user.user_id)
            # print(topic_validation.topic_title)
            topic.validation.append(topic_validation)
            db.session.add(topic_validation)
            db.session.commit()
        else:
            topic_validation.validation = result['validation']
            db.session.commit()
    return jsonify({'status':'success'})
    
    
# Responsible for the card-style of topic validation.
@topic.route('/single_validation/<topic_id>', methods=["GET", "POST"])
@login_required
def single_validation(topic_id):
    selected_topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    return render_template('topic/single_validation.html', topic=selected_topic)


#Responsible for sending filtered resources back to templates of arrange_topics
@topic.route('/filter_resources')
@login_required
def filter_resources():
    topic_id = request.args.get('topic_id', None)
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    resources = db.session.query(Resource).filter(Resource.max_capacity >= topic.max_attendance).all()
    data = dict()
    for resource in resources:
        data[resource.r_id] = resource.name + " (" + str(resource.max_capacity) + ")"
    return jsonify(data)


#Responsible for validating the arrangement submitted by the administrators.
#The validation mainly focuses on avoiding repeated assigned speakers and resources.
#If the result is good, save the schedule.
@topic.route('/validate_arrangement', methods=['GET', 'POST'])
@login_required
def validate_arrangement():
    json_data = request.get_json(force=True)
    schedule = json_data['schedule']
    r_conflict = "Each resource can only be assigned at most one topic at the same time."
    s_conflict = "Each spaker can only give at most one speech at the same time."
    errors = list()
    for s in schedule:
        if speaker_conflict(s['topic_id'], s['date'], s['time_from'], s['time_to']):
            error_msg = dict()
            error_msg['topic_id'] = s['topic_id']
            error_msg['message'] = s_conflict
            errors.append(error_msg)
        if room_conflict(s['topic_id'], s['date'], s['time_from'], s['time_to'], s['resource']):
            error_msg = dict()
            error_msg['topic_id'] = s['topic_id']
            error_msg['message'] = r_conflict
            errors.append(error_msg)
    if not errors:
        for s in schedule:
            topic = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first()
            #print('--------------------')
            #print(topic)
            if topic.schedule.first()==None:
                t_s = TopicSchedule(topic.title, topic.year_start, s['date'], s['date'], \
                datetime.datetime.strptime(s['time_from'], '%H:%M:%S').time(), datetime.datetime.strptime(s['time_to'], '%H:%M:%S').time(), s['resource'], g.user.user_id)
                db.session.add(t_s)
            else:
                t_s = topic.schedule.first()
                t_s.day_from = s['date']
                t_s.day_to = s['date']
                t_s.time_from = datetime.datetime.strptime(s['time_from'], '%H:%M:%S').time()
                t_s.time_to = datetime.datetime.strptime(s['time_to'], '%H:%M:%S').time()
                t_s.resource = s['resource']
        db.session.commit()
        return jsonify({'status':'success'})
    else:
        return jsonify({'ErrorMessage': errors})


#Return all the scheduled info to the place_topic.html through json
@topic.route('/ajax_schedule', methods=['GET', 'POST'])
@login_required
def ajax_schedule():
    all_schedule = TopicSchedule.query.all()
    schedule = list()
    for s in all_schedule:
        each_schedule = dict()
        each_schedule['topic_id'] = s.scheduled_topic.topic_id
        each_schedule['description'] = s.scheduled_topic.description
        each_schedule['topic_title'] = s.topic_title
        each_schedule['year'] = s.topic_year
        from_str = datetime.datetime.combine(s.day_from,s.time_from)
        to_str = datetime.datetime.combine(s.day_from,s.time_to)
        each_schedule['from'] = datetime.datetime.strftime(from_str, "%Y-%m-%d %H:%M:%S")
        each_schedule['to'] = datetime.datetime.strftime(to_str, "%Y-%m-%d %H:%M:%S")
        each_schedule['resource'] = s.assigned_resource.name
        each_schedule['contentFormat'] = s.scheduled_topic.format_type.name + \
            " (" + s.scheduled_topic.content_type.name + ")"
        schedule.append(each_schedule)

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        filter_data = json_data["filters"]
        content_filter = format_filter = location = None
        for f in filter_data:
            if f['type'] == 'content':
                content_filter = f['value']
            if f['type'] == 'format':
                format_filter = f['value']
            if f['type'] == 'location':
                location = f['value']
        filtered_results = content_format_location_filter(content_filter, format_filter, location)
        filtered_topics = filtered_results['topics']
        # print(filtered_topics)
        unscheduled_topics = set(filtered_topics) - set(scheduled_topics)
    else:
        unscheduled_topics = set(Topic.query.all()) - set(scheduled_topics)

    for ut in unscheduled_topics:
        each_schedule = dict()
        each_schedule['topic_id'] = ut.topic_id
        each_schedule['description'] = ut.description
        each_schedule['topic_title'] = ut.title
        each_schedule['year'] = ut.year_start
        each_schedule['from'] = "1970-01-01 00:00:00"
        start_time = datetime.datetime.strptime('2100-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        each_schedule['to'] = datetime.datetime.strftime(start_time + datetime.timedelta(hours=int(ut.hour_duration), minutes=int(ut.minute_duration)), "%Y-%m-%d %H:%M:%S")
        each_schedule['resource'] = 'TBD'
        each_schedule['contentFormat'] = ut.format_type.name + " (" + ut.content_type.name + ")"
        schedule.append(each_schedule)
        #print (each_schedule)
    return json.dumps(schedule)


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


#Check if the speaker has been conflicted
def speaker_conflict(topic_id, date, time_from, time_to):
    scheduled_topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    same_speaker1_topics = set(db.session.query(Topic).filter(Topic.speaker1 == scheduled_topic.speaker1).all())
    same_speaker1_topics = same_speaker1_topics.union(set(db.session.query(Topic).filter(Topic.speaker2 != '').filter(Topic.speaker2 == scheduled_topic.speaker1).all()))
    same_speaker1_topics = same_speaker1_topics.union(set(db.session.query(Topic).filter(Topic.speaker3 != '').filter(Topic.speaker3 == scheduled_topic.speaker1).all()))

    same_speaker_topics = set()
    same_speaker2_topics = set()
    same_speaker3_topics = set()
    if scheduled_topic.speaker2 != '':
        same_speaker2_topics = set(db.session.query(Topic).filter(Topic.speaker1 == scheduled_topic.speaker2).all())
        same_speaker2_topics = same_speaker2_topics.union(set(db.session.query(Topic).filter(Topic.speaker2 != '').filter(Topic.speaker2 == scheduled_topic.speaker2).all()))
        same_speaker2_topics = same_speaker2_topics.union(set(db.session.query(Topic).filter(Topic.speaker3 != '').filter(Topic.speaker3 == scheduled_topic.speaker2).all()))
    if scheduled_topic.speaker3 != '':
        same_speaker3_topics = set(db.session.query(Topic).filter(Topic.speaker1 == scheduled_topic.speaker3).all())
        same_speaker3_topics = same_speaker3_topics.union(set(db.session.query(Topic).filter(Topic.speaker2 != '').filter(Topic.speaker2 == scheduled_topic.speaker3).all()))
        same_speaker3_topics = same_speaker3_topics.union(set(db.session.query(Topic).filter(Topic.speaker3 != '').filter(Topic.speaker3 == scheduled_topic.speaker3).all()))
    same_speaker_topics = same_speaker1_topics.union(same_speaker2_topics).union(same_speaker3_topics)
    same_speaker_topics.discard(scheduled_topic)

    if same_speaker_topics == None:
        return False
    for sst in same_speaker_topics:
        sst_schedules = db.session.query(TopicSchedule).filter(TopicSchedule.topic_title == sst.title).filter(TopicSchedule.topic_year == sst.year_start).all()
        for schedule in sst_schedules:
            if schedule.day_from.strftime('%Y-%m-%d') == date:
                t_to = datetime.datetime.strptime(time_to, '%H:%M:%S').time()
                t_from = datetime.datetime.strptime(time_from, '%H:%M:%S').time()
                if schedule.time_from < t_to and schedule.time_to > t_from:
                    print("S Conflict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return True
    return False


#Check if the resource has been conflicted
def room_conflict(topic_id, date, time_from, time_to, resource):
    scheduled_topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    schedule_topic_schedule = db.session.query(TopicSchedule).join(Resource).filter(TopicSchedule.topic_title == scheduled_topic.title).filter(TopicSchedule.topic_year == scheduled_topic.year_start).first()
    #print(schedule_topic_schedule)
    #print('resource: ' + resource)
    #print(schedule_topic_schedule)
    #print("------------------")
    same_resource_schedule = db.session.query(TopicSchedule).join(Resource).filter(Resource.r_id == resource).all()
    #print(same_resource_schedule)
    if schedule_topic_schedule!= None and resource == schedule_topic_schedule.resource:
        same_resource_schedule.remove(schedule_topic_schedule)
    #print(same_resource_schedule)
    if same_resource_schedule == None:
        return False
    for srs in same_resource_schedule:
        if srs.day_from.strftime('%Y-%m-%d') == date:
            # print('New Date: ' + date)
            t_to = datetime.datetime.strptime(time_to, '%H:%M:%S').time()
            t_from = datetime.datetime.strptime(time_from, '%H:%M:%S').time()
            if srs.time_from < t_to and srs.time_to > t_from:
                print("R Conflict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return True
    #print(same_resource_schedule)
    return False


#Return topics based on the content, format and location
def content_format_location_filter(content_filter, format_filter, location_filter):
    contents = db.session.query(Content).all()
    formats = db.session.query(Format).all()
    locations_set = db.session.query(Topic.location).all()
    content_names = list()
    format_names = list()
    locations = list()
    results = dict()
    for c in contents:
        content_names.append(str(c.name))
    for f in formats:
        format_names.append(str(f.name))
    for l in locations_set:
        l_name = str(l[0])
        if l_name not in locations:
            locations.append(l_name)

    topics_content = topics_format = topics_location = db.session.query(Topic).all()
    if content_filter != None:
        topics_content = db.session.query(Content).filter(Content.name == content_filter).first().topics.all()
    if format_filter != None:
        topics_format = db.session.query(Format).filter(Format.name == format_filter).first().topics.all()
    if location_filter != None:
        topics_location = db.session.query(Topic).filter(Topic.location == location_filter).all()
    topics = set(topics_format).intersection(topics_content).intersection(topics_location)

    results['content_names'] = content_names
    results['format_names'] = format_names
    results['locations'] = locations
    results['topics'] = topics
    return results


#Refresh the global variable before every request
@topic.before_request
def before_request():
    g.user = current_user


#Generate the topic id.
#Topic id is length of 6 with random characters.
def generate_topic_id():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 6)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3] + candidate[4] + candidate[5]
    return str(active_code)