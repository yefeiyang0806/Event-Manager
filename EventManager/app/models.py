from app import db
import time, uuid

class User(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    email = db.Column(db.String(40), index = True, unique = True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    events = db.relationship('Event', backref='author', lazy='dynamic')
    status = db.Column(db.Integer, default=0)
    active_code = db.Column(db.String(4))
    role_id = db.Column(db.String(40), db.ForeignKey('role.uuid'))


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


    def __init__(self, email, password, first_name, last_name, active_code):
        self.uuid = str(uuid.uuid1())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.active_code = active_code
        self.status = 0
        role = db.session.query(Role.uuid).filter(Role.rolename == "normal").first()
        self.role_id = str(role.uuid)


class Event(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    topic = db.Column(db.String(40))
    short_text = db.Column(db.String(40))
    description = db.Column(db.String(200))
    min_attendance = db.Column(db.Integer)
    max_attendance = db.Column(db.Integer)
    speaker = db.Column(db.String(40))
    year_start = db.Column(db.String(4))
    month_start = db.Column(db.String(2))
    day_start = db.Column(db.String(2))
    day_duration = db.Column(db.String(3))
    hour_duration = db.Column(db.String(2))
    minute_duration = db.Column(db.String(2))

    status = db.Column(db.String(2), default='NA')
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(40), db.ForeignKey('user.email'))
    content = db.Column(db.String(40), db.ForeignKey('content.name'))
    format = db.Column(db.String(40), db.ForeignKey('format.name'))
    schedule = db.relationship('EventSchedule', backref='scheduled_event', lazy='dynamic')
    score = db.relationship('EventScore', backref='scored_event', lazy='dynamic')

    __table_args__ = (db.UniqueConstraint('topic', 'year_start', name='_topic_year_start_uc'),)

    
    def __repr__(self):
        return '<Event %r>' %(self.topic)


    def __init__(self, topic, short_text, description, min_attendance, max_attendance, speaker, year_start, month_start, day_start, day_duration, hour_duration, minute_duration, create_by, content, format):
        self.uuid = str(uuid.uuid1())
        self.topic = topic
        self.short_text = short_text
        self.description = description
        self.min_attendance = min_attendance
        self.max_attendance = max_attendance
        self.speaker = speaker
        self.year_start = year_start
        self.month_start = month_start
        self.day_start = day_start
        self.day_duration = day_duration
        self.hour_duration = hour_duration
        self.minute_duration = minute_duration
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.status = 0
        print(create_by)
        create_user = db.session.query(User).filter(User.email == create_by).first()
        input_content = db.session.query(Content).filter(Content.name == content).first()
        input_format = db.session.query(Format).filter(Format.name == format).first()
        create_user.events.append(self)
        input_content.events.append(self)
        input_format.events.append(self)


    def is_created_by(self, user_email):
        if self.create_by == user_email:
            return True

        else:
            return False


class Role_menu(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    role_id = db.Column(db.String(40), db.ForeignKey('role.uuid'), primary_key = True)
    menu_id = db.Column(db.String(40), db.ForeignKey('menu.uuid'), primary_key = True)
    menu = db.relationship("Menu", backref="role_assoc")

    def __repr__(self):
        return '<Role_Menu %r>' % (self.uuid)


    def __init__(self, role_id, menu_id):
        self.role_id = role_id
        self.menu_id = menu_id
        self.uuid = str(uuid.uuid1())


class Menu(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    menu = db.Column(db.String(40), index = True, unique = True)
    menu_path = db.Column(db.String(40))


    def __repr__(self):
        return '<User %r>' % (self.menu)


    def __init__(self, menu, menu_path):
        self.uuid = str(uuid.uuid1())
        self.menu = menu
        self.menu_path = menu_path


class Role(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    rolename = db.Column(db.String(20), index = True, unique = True)
    description = db.Column(db.String(40))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(20))
    menus = db.relationship("Role_menu", backref='role')

    
    def __repr__(self):
        return '<Role %r>' %(self.rolename)


    def __init__(self, rolename, description,create_by):
        self.uuid = str(uuid.uuid1())
        self.rolename=rolename
        self.description = description
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by


class ResourceType(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    name = db.Column(db.String(10), index=True, unique=True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(20))
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
    content_id = db.Column(db.String(20))
    name = db.Column(db.String(20), index=True, unique=True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(20))
    events = db.relationship('Event', backref='content_type', lazy='dynamic')


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
    format_id = db.Column(db.String(20))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(40))
    events = db.relationship('Event', backref='format_type', lazy='dynamic')


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
    create_by = db.Column(db.String(40))
    r_type = db.Column(db.String(40), db.ForeignKey('resource_type.uuid'))
    schedule = db.relationship('EventSchedule', backref='assigned_resource', lazy='dynamic')


    def __repr__(self):
        return '<Resource %r>' %(self.name)


    def __init__(self, name, create_by, resource_type):
        self.uuid = str(uuid.uuid1())
        self.name=name
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.create_by = create_by
        self.resource_type = resource_type.uuid


class EventSchedule(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    event_topic = db.Column(db.String(40))
    event_year = db.Column(db.String(4))
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['event_topic', 'event_year'],
            ['event.topic', 'event.year_start'],
        ),
    )

    day_from = db.Column(db.Date, nullable=True)
    day_to = db.Column(db.Date, nullable=True)
    time_from = db.Column(db.Time, nullable=True)
    time_to = db.Column(db.Time, nullable=True)

    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(40))
    resource = db.Column(db.String(20), db.ForeignKey('resource.r_id'))


    def __repr__(self):
        return '<EventSchedule %r>' %(self.event_topic)


    def __init__(self, event_topic, event_year, day_from, day_to, time_from, time_to, resource, create_by):
        related_resource = db.session.query(Resource).filter(Resource.r_id == resource).first()
        related_resource.schedule.append(self)
        scheduled_event = db.session.query(Event).filter(Event.topic == event_topic).filter(Event.year_start == event_year).first()
        scheduled_event.schedule.append(self)

        self.uuid = str(uuid.uuid1())
        self.day_from = day_from
        self.day_to = day_to
        self.time_from = time_from
        self.time_to = time_to
        self.event = event
        self.create_by = create_by
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")


class EventScore(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    event_topic = db.Column(db.String(40))
    event_year = db.Column(db.String(4))
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['event_topic', 'event_year'],
            ['event.topic', 'event.year_start'],
        ),
    )
    score =  db.Column(db.Integer)
    agent = db.Column(db.String(40))
    create_time = db.Column(db.Time)
    create_date = db.Column(db.Date)
    

    def __repr__(self):
        return '<EventScore %r>' %(self.event_topic)

    def __init__(self, event_topic, event_year, score, agent, create_time, create_date):
        self.uuid = str(uuid.uuid1())
        self.score = score
        self.agent = agent
        self.create_time = create_time
        self.create_date = create_date

        scored_event = db.session.query(Event).filter(Event.topic == event_topic).filter(Event.year_start == event_year).first()
        scored_event.score.append(self)

        