from app import db
import time, uuid

class User(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    user_id = db.Column(db.String(10), index=True, unique = True)
    email = db.Column(db.String(40), index = True, unique = True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    full_name = db.Column(db.String(60))
    department = db.Column(db.String(40))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    created_topics = db.relationship('Topic', backref='author', lazy='dynamic')
    topics_to_speak = db.relationship('Topic', backref='speaker')
    status = db.Column(db.Integer, default=0)
    active_code = db.Column(db.String(4))
    role_id = db.Column(db.String(40), db.ForeignKey('role.role_id'))


    def is_authenticated(self):
    	return True


    def is_active(self):
    	return True


    def is_anonymous(self):
    	return False


    def get_id(self):
    	try:
    		return unicode(self.uuid)
    	except NameError:
    		return str(self.uuid)


    def __repr__(self):
        return '<User %r>' % (self.username)


    def __init__(self, user_id, email, password, first_name, last_name, department, active_code):
        self.uuid = str(uuid.uuid1())
        self.user_id = user_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + ' ' + last_name
        self.department = department
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.active_code = active_code
        self.status = 0
        related_role = db.session.query(Role.uuid).filter(Role.rolename == "normal").first()
        related_role.append(self)


class Topic(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    topic_id = db.Column(db.String(10))
    title = db.Column(db.String(255))
    description = db.Column(db.String(400))
    min_attendance = db.Column(db.Integer)
    max_attendance = db.Column(db.Integer)
    year_start = db.Column(db.String(4))
    month_start = db.Column(db.String(2))
    day_start = db.Column(db.String(2))
    day_duration = db.Column(db.String(3))
    hour_duration = db.Column(db.String(2))
    minute_duration = db.Column(db.String(2))

    status = db.Column(db.String(2), default='NA')
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    speaker1 = db.Column(db.String(10), db.ForeignKey('user.user_id'))
    speaker2 = db.Column(db.String(10), nullable=True)
    speaker3 = db.Column(db.String(10), nullable=True)
    create_by = db.Column(db.String(10), db.ForeignKey('user.user_id'))
    content = db.Column(db.String(40), db.ForeignKey('content.content_id'))
    format = db.Column(db.String(40), db.ForeignKey('format.format_id'))
    link = db.Column(db.String(60))
    jamlink = db.Column(db.String(60))

    location = db.Column(db.String(30))
    schedule = db.relationship('TopicSchedule', backref='scheduled_topic', lazy='dynamic')
    validation = db.relationship('TopicValidation', backref='validated_topic', lazy='dynamic')
    
    __table_args__ = (db.UniqueConstraint('title', 'year_start', name='_title_year_start_uc'),)

    
    def __repr__(self):
        return '<Topic %r>' %(self.topic)


    def __init__(self, title, description, min_attendance, max_attendance, speaker1, speaker2, speaker3, year_start, month_start, day_start, \
        day_duration, hour_duration, minute_duration, create_by, content_id, format_id, location):
        self.uuid = str(uuid.uuid1())
        self.title = title
        self.description = description
        self.min_attendance = min_attendance
        self.max_attendance = max_attendance
        self.speaker1 = speaker1
        self.speaker2 = speaker2
        self.speaker3 = speaker3
        self.year_start = year_start
        self.month_start = month_start
        self.day_start = day_start
        self.day_duration = day_duration
        self.hour_duration = hour_duration
        self.minute_duration = minute_duration
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.status = 0
        self.location=location

        create_user = db.session.query(User).filter(User.user_id == create_by).first()
        input_content = db.session.query(Content).filter(Content.content_id == content_id).first()
        input_format = db.session.query(Format).filter(Format.format_id == format_id).first()
        
        same_format_topic_count = db.session.query(Topic).filter(Topic.format == input_format.format_id).count()
        self.topic_id = input_format.format_id + "-" + same_format_topic_count
        

        create_user.created_topics.append(self)
        input_content.created_topics.append(self)
        input_format.created_topics.append(self)



    def is_created_by(self, user_id):
        if self.create_by == user_id:
            return True

        else:
            return False


class Role_menu(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    role_id = db.Column(db.String(10), db.ForeignKey('role.role_id'), primary_key = True)
    menu_id = db.Column(db.String(10), db.ForeignKey('menu.menu_id'), primary_key = True)
    menu = db.relationship("Menu", backref="role_assoc")
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))

    def __repr__(self):
        return '<Role_Menu %r>' % (self.uuid)


    def __init__(self, role_id, menu_id, create_by):
        self.role_id = role_id
        self.menu_id = menu_id
        self.uuid = str(uuid.uuid1())
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class Menu(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    menu = db.Column(db.String(40), index = True, unique = True)
    menu_id = db.Column(db.String(10), index = True, unique = True)
    menu_path = db.Column(db.String(40))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))


    def __repr__(self):
        return '<User %r>' % (self.menu)


    def __init__(self, menu, menu_id, menu_path, create_by):
        self.uuid = str(uuid.uuid1())
        self.menu = menu
        self.menu_id = menu_id
        self.menu_path = menu_path
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class Role(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    rolename = db.Column(db.String(20), index = True, unique = True)
    role_id = db.Column(db.String(10), index = True, unique = True)
    description = db.Column(db.String(40))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    menus = db.relationship("Role_menu", backref='role')

    
    def __repr__(self):
        return '<Role %r>' %(self.rolename)


    def __init__(self, rolename, role_id, description,create_by):
        self.uuid = str(uuid.uuid1())
        self.rolename=rolename
        self.role_id = role_id
        self.description = description
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class ResourceType(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    name = db.Column(db.String(10), index=True, unique=True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    related_resources = db.relationship('Resource', backref='resource_type', lazy='dynamic')


    def __repr__(self):
        return '<ResourceType %r>' %(self.name)


    def __init__(self, name, create_by):
        self.uuid = str(uuid.uuid1())
        self.name=name
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by



class Content(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    content_id = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(20), index=True, unique=True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    topics = db.relationship('Topic', backref='content_type', lazy='dynamic')


    def __repr__(self):
        return '<Content %r>' %(self.name)


    def __init__(self, name, content_id, create_by):
        self.uuid = str(uuid.uuid1())
        self.name=name
        self.content_id = content_id
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class Format(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    name = db.Column(db.String(20), index=True, unique=True)
    format_id = db.Column(db.String(20), unique = True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    topics = db.relationship('Topic', backref='format_type', lazy='dynamic')


    def __repr__(self):
        return '<Format %r>' %(self.name)


    def __init__(self, name, create_by, format_id):
        self.uuid = str(uuid.uuid1())
        self.name=name
        self.format_id = format_id
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class Resource(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    name = db.Column(db.String(20), index=True, unique=True)
    r_id = db.Column(db.String(20), index=True, unique=True)
    r_description = db.Column(db.String(40))
    max_capacity = db.Column(db.Integer)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    r_type = db.Column(db.String(40), db.ForeignKey('resource_type.uuid'))
    schedule = db.relationship('TopicSchedule', backref='assigned_resource', lazy='dynamic')


    def __repr__(self):
        return '<Resource %r>' %(self.name)


    def __init__(self, name, create_by, resource_type):
        self.uuid = str(uuid.uuid1())
        self.name=name
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by
        self.resource_type = resource_type.uuid


class TopicSchedule(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    topic_title = db.Column(db.String(255))
    topic_year = db.Column(db.String(4))
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['topic_title', 'topic_year'],
            ['topic.title', 'topic.year_start'],
        ),
    )

    day_from = db.Column(db.Date, nullable=True)
    day_to = db.Column(db.Date, nullable=True)
    time_from = db.Column(db.Time, nullable=True)
    time_to = db.Column(db.Time, nullable=True)

    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(10))
    resource = db.Column(db.String(20), db.ForeignKey('resource.r_id'))


    def __repr__(self):
        return '<TopicSchedule %r>' %(self.topic_topic)


    def __init__(self, topic_title, topic_year, day_from, day_to, time_from, time_to, resource, create_by):
        related_resource = db.session.query(Resource).filter(Resource.r_id == resource).first()
        related_resource.schedule.append(self)
        scheduled_topic = db.session.query(Topic).filter(Topic.title == topic_title).filter(topic.year_start == topic_year).first()
        scheduled_topic.schedule.append(self)

        self.uuid = str(uuid.uuid1())
        self.day_from = day_from
        self.day_to = day_to
        self.time_from = time_from
        self.time_to = time_to
        self.create_by = create_by
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")


class TopicValidation(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    topic_title = db.Column(db.String(255))
    topic_year = db.Column(db.String(4))
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['topic_title', 'topic_year'],
            ['topic.title', 'topic.year_start'],
        ),
    )
    validation =  db.Column(db.Integer)
    agent = db.Column(db.String(10))
    create_time = db.Column(db.Time)
    create_date = db.Column(db.Date)
    

    def __repr__(self):
        return '<TopicValidation %r>' %(self.topic_title)

    def __init__(self, topic_title, topic_year, validation, agent):
        self.uuid = str(uuid.uuid1())
        self.validation = validation
        self.agent = agent
        self.create_time = create_time
        self.create_date = create_date
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")

        validated_topic = db.session.query(Topic).filter(Topic.title == topic_title).filter(Topic.year_start == topic_year).first()
        validated_topic.validation.append(self)

        