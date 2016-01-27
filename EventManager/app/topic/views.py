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
import random, json, datetime, math, xlwt
import re


topic = Blueprint('topic', __name__)
full_name = ''
status = ''
menu_categories = list()


# Responsible for creating topics.
@topic.route('/create', methods = ['GET', 'POST'])
@login_required
def create_topic():
    user_id = g.user.user_id
    # menus = menus_of_role()
    form = CreateTopicForm()
    form.set_options()   
    
    if form.validate_on_submit():      
        startdata = form.DateStart.data.split('-')
        year_start = startdata[0]
        month_start = startdata[1]
        day_start = startdata[2]
        new_topic_id = generate_topic_id()
        while db.session.query(Topic).filter(Topic.topic_id == new_topic_id).first() is not None:
            new_topic_id = generate_topic_id()
        temp = Topic(new_topic_id, form.title.data, form.description.data, form.min_attendance.data, form.max_attendance.data,\
                form.speaker1.data, form.speaker2.data, form.speaker3.data, form.speaker4.data, form.speaker5.data, year_start, month_start, day_start,\
                form.day_duration.data, form.hour_duration.data, form.minute_duration.data, g.user.email,\
                form.content.data, form.format.data, form.location.data, form.link.data, form.jamlink.data, form.memo.data)     
        db.session.add(temp)
        db.session.commit()
        #print (db.session.query(Content).filter(Content.name == form.content.data).first().topics.count())user_email, 
        return redirect(url_for('basic.logged_in'))
    return render_template("topic/create_topic.html", form=form, full_name=full_name, status=status, menu_categories=menu_categories)


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
    form = CreateTopicForm()
    form.set_options()
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
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
            # menus = menus_of_role()
            return render_template("topic/modify_topic.html", form=form,\
                full_name=full_name, status=status, topic_id=topic_id, menu_categories=menu_categories)

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
        # menus = menus_of_role()
        return render_template("topic/modify_topic.html", form=form, full_name=full_name, status=status, \
            topic_id=topic_id, menu_categories=menu_categories, speaker1_name=speaker1_name, speaker2_name=speaker2_name, \
            speaker3_name=speaker3_name, speaker4_name=speaker4_name, speaker5_name=speaker5_name)
    return redirect(url_for("basic.index"))



#Reached by the link on the topics' titles. Show details of the selected topic
@topic.route('/view')
@login_required
def view_topic():
    # menus = menus_of_role()
    topic_id = request.args.get('topic_id')
    topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    if topic.is_created_by(g.user.email):
        mode = 'creator'
    else:
        mode = 'viewer'
    return render_template('topic/view_topic.html', topic=topic, mode=mode, full_name=full_name,\
        status=status, menu_categories=menu_categories)


#Show all the available topics in the website.
#Once finished, should only show approved topics
@topic.route('/available')
@login_required
def available_topics():
    page_number = request.args.get('page', None)
    # menus = menus_of_role()
    topic_number = db.session.query(Topic).count()
    page_count = math.ceil(topic_number/10)
    if page_number is None:
        topics = db.session.query(Topic).order_by(Topic.format).limit(10)
    else:
        offset_pages = int(page_number)-1
        topics = db.session.query(Topic).order_by(Topic.format).offset(offset_pages*10).limit(10)
    return render_template('topic/available_topics.html', topics=topics, full_name=full_name, status=status, menu_categories=menu_categories, page_count=page_count)


#Show the page of scheduling all the approved topics. The page is reached by the "Arrange topic link in the topic management side bar"
@topic.route('/arrange')
@login_required
def arrange_topics():
    # menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    keyword = request.args.get('keyword', None)
    results = topic_filters(content_filter, format_filter, location_filter, keyword)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    rejected_topics = db.session.query(Topic).filter(Topic.status=='RJ').all()
    topics = set(results['topics'].all())
    topics = set(topics).difference(set(rejected_topics))
    
    return render_template('topic/arrange_topics.html', topics=topics, full_name=full_name, status=status, \
        menu_categories=menu_categories, content_names=content_names, format_names=format_names, locations=locations)


#Show the page of scheduling all the approved topics. The page is reached by the "Place topic link in the topic management side bar"
@topic.route('/place')
@login_required
def place_topics():
    # menus = menus_of_role()
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    keyword = None
    results = topic_filters(content_filter, format_filter, location_filter, keyword)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    return render_template('topic/place_topics.html', full_name=full_name, status=status, \
        menu_categories=menu_categories, content_names=content_names, format_names=format_names, locations=locations)


#Show the page of scheduling all the approved topics. The page is reached by the "validate topic" link in the topic management side bar"
@topic.route('/validate')
@login_required
def validate_topics():
    # menus = menus_of_role()
    page_number = request.args.get('page', None)
    content_filter = request.args.get('content', None)
    format_filter = request.args.get('format', None)
    location_filter = request.args.get('location', None)
    keyword = request.args.get('keyword', None)
    results = topic_filters(content_filter, format_filter, location_filter, keyword)
    content_names = results['content_names']
    format_names = results['format_names']
    locations = results['locations']
    topics = results['topics']
    rejected_topics = db.session.query(Topic.topic_id).filter(Topic.status == 'RJ')
    approved_topics = db.session.query(Topic.topic_id).filter(Topic.status == 'AP')
    #topics = topics.filter(~Topic.topic_id.in_(rejected_topics)).filter(~Topic.topic_id.in_(approved_topics))
    topic_count = topics.count()
    page_count = math.ceil(topic_count/10)
    if page_number is None:
        topics = topics.order_by(Topic.format).limit(10)
    else:
        offset_pages = int(page_number)-1
        topics = topics.order_by(Topic.format).offset(offset_pages*10).limit(10)
    return render_template('topic/validate_topics.html', topics=topics, full_name=full_name, status=status, \
        menu_categories=menu_categories, content_names=content_names, format_names=format_names, locations=locations, page_count=page_count)
        

# Handle the content sent from the templates to insert validation result into db.
@topic.route('/ajax_validation', methods=["GET", "POST"])
@login_required
def ajax_validation():
    json_data = request.get_json(force=True)
    results = json_data["Results"]
    for result in results:
        topic_validation = db.session.query(TopicValidation).filter(TopicValidation.topic_id == result['topic_id']).first()
        if topic_validation == None:
            topic_validation = TopicValidation(result['topic_id'], result['validation'], g.user.user_id)
            topic = db.session.query(Topic).filter(Topic.topic_id == result['topic_id']).first()
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
    speakers_list = list()
    speaker1 = db.session().query(User).filter(User.user_id == selected_topic.speaker1).first()
    speaker2 = db.session().query(User).filter(User.user_id == selected_topic.speaker2).first()
    speaker3 = db.session().query(User).filter(User.user_id == selected_topic.speaker3).first()
    speaker4 = db.session().query(User).filter(User.user_id == selected_topic.speaker4).first()
    speaker5 = db.session().query(User).filter(User.user_id == selected_topic.speaker5).first()
    if speaker1 is not None:
        speakers_list.append(speaker1)
    if speaker2 is not None:
        speakers_list.append(speaker2)
    if speaker3 is not None:
        speakers_list.append(speaker3)
    if speaker4 is not None:
        speakers_list.append(speaker4)
    if speaker5 is not None:
        speakers_list.append(speaker5)
    return render_template('topic/single_validation.html', topic=selected_topic, speakers_list=speakers_list)


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
        #Remove schedule results of modified topics
        topic = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first()
        already_schedule = db.session.query(TopicSchedule).filter(TopicSchedule.scheduled_topic==topic).all()
        if already_schedule is not None:
            for als in already_schedule:
                db.session.delete(als)
                print('----------------schedule deleted------------')
            db.session.commit()
    # Do validations on modifications of schedule
    for s in schedule:
        if s['resource'] == 'TBD':
            topic = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first()
            if topic.schedule.first()!=None:
                db.session.delete(topic.schedule.first())
                db.session.commit()
            # return jsonify({'status':'success'})
        else:
            conflict_speaker = speaker_conflict(s['topic_id'], s['date'], s['time_from'], s['time_to'])
            conflict_room = room_conflict(s['topic_id'], s['date'], s['time_from'], s['time_to'], s['resource'])
            if conflict_speaker:
                error_msg = dict()
                error_msg['topic_id'] = s['topic_id']
                error_msg['title'] = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first().title
                error_msg['message'] = s_conflict
                errors.append(error_msg)
            if conflict_room:
                error_msg = dict()
                error_msg['topic_id'] = s['topic_id']
                error_msg['title'] = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first().title
                error_msg['message'] = r_conflict
                errors.append(error_msg)
            if (not conflict_speaker) and (not conflict_room):
                topic = db.session.query(Topic).filter(Topic.topic_id == s['topic_id']).first()
                if topic.schedule.first()==None:
                    t_s = TopicSchedule(topic.topic_id, s['date'], s['date'], \
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
    if not errors:
        return jsonify({'status':'success'})
    else:
        return jsonify({'ErrorMessage': errors})


#Return all the scheduled info to the place_topic.html through json
@topic.route('/ajax_schedule', methods=['GET', 'POST'])
@login_required
def ajax_schedule():
    all_schedule = TopicSchedule.query.all()
    schedule = list()
    scheduled_topics = list()
    for s in all_schedule:
        each_schedule = dict()
        scheduled_topics.append(s.scheduled_topic)
        each_schedule['topic_id'] = s.topic_id
        each_schedule['description'] = s.scheduled_topic.description
        each_schedule['topic_title'] = s.scheduled_topic.title
        each_schedule['year'] = s.scheduled_topic.year_start
        from_str = datetime.datetime.combine(s.day_from,s.time_from)
        to_str = datetime.datetime.combine(s.day_from,s.time_to)
        each_schedule['from'] = datetime.datetime.strftime(from_str, "%Y-%m-%d %H:%M:%S")
        each_schedule['to'] = datetime.datetime.strftime(to_str, "%Y-%m-%d %H:%M:%S")
        each_schedule['resource'] = s.assigned_resource.r_id
        each_schedule['contentFormat'] = s.scheduled_topic.format_type.name + \
            " (" + s.scheduled_topic.content_type.name + ")"
        schedule.append(each_schedule)

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        filter_data = json_data["filters"]
        content_filter = format_filter = location = keyword = None
        for f in filter_data:
            if f['type'] == 'content':
                content_filter = f['value']
            if f['type'] == 'format':
                format_filter = f['value']
            if f['type'] == 'location':
                location_filter = f['value']
            if f['type'] == 'keyword':
                keyword = f['value']
        filtered_results = topic_filters(content_filter, format_filter, location_filter, keyword)
        rejected_topics = db.session.query(Topic).filter(Topic.status=='RJ').all()
        filtered_topics = filtered_results['topics']
        filtered_topics = set(filtered_topics).difference(set(rejected_topics))
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


#Remove all the schedule records based on the passed filter conditions
@topic.route('/reset_schedule', methods=['GET', 'POST'])
@login_required
def reset_schedule():
    json_data = request.get_json(force=True)
    conditions = json_data["remove_conditions"]
    content_filter = format_filter = location = keyword = None
    for f in conditions:
        if f['type'] == 'content':
            content_filter = f['value']
        if f['type'] == 'format':
            format_filter = f['value']
        if f['type'] == 'location':
            location_filter = f['value']
        if f['type'] == 'keyword':
            keyword = f['value']
    filtered_results = topic_filters(content_filter, format_filter, location_filter, keyword)
    filtered_topics = filtered_results['topics'].all()
    related_topic_id = list()
    for t in filtered_topics:
        related_topic_id.append(t.topic_id)
    related_schedules = db.session.query(TopicSchedule).filter(TopicSchedule.topic_id.in_(related_topic_id)).all()
    for rs in related_schedules:
        # print(rs.topic_id)
        db.session.delete(rs)
    db.session.commit()
    return 'success'


#Return all the resources info to the place_topic.html through json
@topic.route('/ajax_resources/<format>', methods=['GET', 'POST'])
@topic.route('/ajax_resources', methods=['GET', 'POST'])
@login_required
def ajax_resources(format=None):
    res = list()
    if format is None:
        selected_resources = db.session.query(Resource).all()
    else:
        formats = format.split(',')
        formats_names = list()
        for f in formats:
            if f != '':
                name = db.session.query(Format).filter(Format.format_id == f).first().name
                formats_names.append(name)
        # formats_names = db.session.query(Format).filter(Format.format_id.in_(formats)).all()
        print ("-------------------------")
        print(formats)
        print (formats_names[0])
        selected_resources = db.session.query(Resource).filter(Resource.r_type.in_(formats_names)).all()
    for r in selected_resources:
        each_r = dict()
        each_r['resource'] = r.r_id
        res.append(each_r)
    res.append({'resource': 'TBD'})
    return json.dumps(res)


# Go to the page to show the results of schedule
@topic.route('/schedule_output')
@login_required
def schedule_output():
    output_schedule()
    return redirect(url_for("basic.index"))


#Required by the LoginManager
@lm.user_loader
def load_user(id):
    return User.query.get(str(id))


def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menu_categories = list()
    cat_grouped_menus = list()
    category_ids = list()
    for m in middles:
        certain_menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        if certain_menu.category_id not in category_ids:
            category_ids.append(certain_menu.category_id)
            cat_grouped_menus.append(certain_menu)
    for c in cat_grouped_menus:
        c_menus = list()
        cat = dict()
        cat['category_id'] = c.category_id
        cat['category_name'] = c.category_name
        menus = db.session.query(Menu).filter(Menu.category_id == c.category_id).all()
        for m in menus:
            each_menu = dict()
            each_menu['menu_id'] = m.menu_id
            each_menu['menu_name'] = m.menu_name
            each_menu['url'] = m.url
            c_menus.append(each_menu)
        cat['menus'] = c_menus
        menu_categories.append(cat)

    # print (menu_categories)
    return menu_categories


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
        sst_schedules = db.session.query(TopicSchedule).filter(TopicSchedule.topic_id == sst.topic_id).all()
        for schedule in sst_schedules:
            if schedule.day_from.strftime('%Y-%m-%d') == date:
                t_to = datetime.datetime.strptime(time_to, '%H:%M:%S').time()
                t_from = datetime.datetime.strptime(time_from, '%H:%M:%S').time()
                if (schedule.time_from < t_to) and (schedule.time_to > t_from):
                    print("S Conflict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return True
    return False


#Check if the resource has been conflicted
def room_conflict(topic_id, date, time_from, time_to, resource):
    scheduled_topic = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
    schedule_topic_schedule = db.session.query(TopicSchedule).join(Resource).filter(TopicSchedule.topic_id == scheduled_topic.topic_id).first()
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
            if (srs.time_from < t_to) and (srs.time_to > t_from):
                print("R Conflict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return True
    #print(same_resource_schedule)
    return False


#Return topics based on the content, format and location
def topic_filters(content_filter, format_filter, location_filter, keyword):
    contents = db.session.query(Content).all()
    formats = db.session.query(Format).all()
    locations_set = db.session.query(Topic.location).all()
    content_names = list()
    format_names = list()
    locations = list()
    results = dict()
    for c in contents:
        content_names.append({'name': str(c.name), 'id': str(c.content_id)})
    for f in formats:
        format_names.append({'name': str(f.name), 'id': str(f.format_id)})
    for l in locations_set:
        l_name = str(l[0])
        if l_name not in locations:
            locations.append(l_name)

    topics = db.session.query(Topic)
    if content_filter != None:
        cfs = content_filter.split(',')
        q_cfs = db.session.query(Topic.topic_id).filter(db.false())
        for cf in cfs:
            q_cf = db.session.query(Topic.topic_id).filter(Topic.content == cf)
            q_cfs = q_cfs.union(q_cf)
        topics = topics.filter(Topic.topic_id.in_(q_cfs))
    if format_filter != None:
        ffs = format_filter.split(',')
        q_ffs = db.session.query(Topic.topic_id).filter(db.false())
        for ff in ffs:
            q_ff = db.session.query(Topic.topic_id).filter(Topic.format == ff)
            q_ffs = q_ffs.union(q_ff)
        topics = topics.filter(Topic.topic_id.in_(q_ffs))
    if location_filter != None:
        lfs = location_filter.split(',')
        q_lfs = db.session.query(Topic.topic_id).filter(db.false())
        for lf in lfs:
            q_lf = db.session.query(Topic.topic_id).filter(Topic.location == lf)
            q_lfs = q_lfs.union(q_lf)
        topics = topics.filter(Topic.topic_id.in_(q_lfs))

    if keyword != None:
        keyword = "%" + keyword + "%"
        topics = topics.filter(Topic.title.ilike(keyword))

    results['content_names'] = content_names
    results['format_names'] = format_names
    results['locations'] = locations
    results['topics'] = topics
    return results


#Refresh the global variable before every request
@topic.before_request
def before_request():
    g.user = current_user
    global full_name, status, menu_categories
    if hasattr(g.user, 'full_name'):
        full_name = g.user.full_name
    if hasattr(g.user, 'status'):
        status = g.user.status
        menu_categories = menus_of_role()


#Generate the topic id.
#Topic id is length of 6 with random characters.
def generate_topic_id():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 6)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3] + candidate[4] + candidate[5]
    return str(active_code)


#Export the schedule to the xls.
def output_schedule():
    content_obj_list = db.session.query(Content.content_id).all()
    content_list = [c[0] for c in content_obj_list]
    # print (content_list)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    style_str = 'align: wrap on, vert top; pattern: pattern solid;'
    
    results = schedule_output()
    start = datetime.datetime.strptime("01/01/16 10:00", "%d/%m/%y %H:%M")
    # print (start.strftime('%H:%M'))
    ws.write(0, 0, 'Resource')
    row_index = 1
    time_interval = datetime.timedelta(minutes=5)
    while start.hour < 20:
        ws.write(row_index, 0, start.strftime('%H:%M'))
        row_index += 1
        start += time_interval
    col_index = 1
    for res_bucket in results:
        row_index = 0
        ws.write(row_index, col_index, res_bucket['res_id'])
        current_hour = 10
        current_minute = 0
        for each_schedule in res_bucket['schedules']:
            row_index += 1
            hour = int(each_schedule['from_hour'])
            minute = int(each_schedule['from_minute'])
            duration = int(each_schedule['duration'])
            # print(current_minute)
            # print(minute)
            color_number = content_list.index(each_schedule['content'])+1
            print(color_number)
            print(each_schedule['content'])
            # To avoid black 0 and 8.
            # if color_number == 1:
                # color_number = 30
            style0 = xlwt.easyxf(style_str)
            style0.pattern.pattern_fore_colour = color_number
            minute_diff = minute - current_minute
            hour_diff = 0
            empty_slots = 0
            rowspan = int(duration/5)
            if minute_diff < 0:
                hour_diff = hour - 1 - current_hour
                minute_diff += 60
            else:
                hour_diff = hour - current_hour
            empty_slots = int((minute_diff + hour_diff * 60) / 5)
            row_index += empty_slots
            ws.write_merge(row_index, int(row_index+rowspan-1), col_index, col_index, each_schedule['title'], style0)
            new_minute = minute + duration
            new_hour = hour
            row_index += rowspan-1
            # Update current time.
            while new_minute >= 60:
                new_minute -= 60
                new_hour += 1
            current_hour = new_hour
            current_minute = new_minute
        col_index += 1


    wb.save('example.xls')



#Output the schedule to a new page
# @topic.route('/schedule_output_ajax')
# @login_required
def schedule_output():
    schedules = db.session.query(TopicSchedule).order_by(TopicSchedule.resource, TopicSchedule.time_from).all()
    current_res = schedules[0].resource
    results = list()
    res_bucket = dict()
    res_bucket['res_id'] = current_res
    schedules_ajax = list()
    for s in schedules:
        related_topic = db.session.query(Topic).filter(Topic.topic_id == s.topic_id).first()
        from_str = datetime.datetime.combine(s.day_from,s.time_from)
        to_str = datetime.datetime.combine(s.day_from,s.time_to)
        delta = to_str - from_str
        appointment = dict()
        appointment['title'] = related_topic.title
        appointment['content'] = related_topic.content
        appointment['topic_id'] = related_topic.topic_id
        appointment['resource'] = s.resource
        appointment['from_hour'] = int(s.time_from.hour)
        appointment['from_minute'] = int(s.time_from.minute)
        appointment['duration'] = int(delta.seconds/60)
        
        if ('res_id' in res_bucket) and (s.resource != res_bucket['res_id']):
            res_bucket['schedules'] = schedules_ajax
            results.append(res_bucket)
            res_bucket = {}
            schedules_ajax = []
        res_bucket['res_id'] = s.resource
        schedules_ajax.append(appointment)
    # Insert the last same resource bucket into results.
    res_bucket['schedules'] = schedules_ajax
    results.append(res_bucket)
    return results
