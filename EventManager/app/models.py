from app import db
import time, uuid

class User(db.Model):
    uuid = db.Column(db.String(40), primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
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
    topic = db.Column(db.String(40), index = True, unique = True)
    description = db.Column(db.String(200))
    min_attendance = db.Column(db.Integer)
    max_attendance = db.Column(db.Integer)
    speaker = db.Column(db.String(40))
    status = db.Column(db.Integer, default=0)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(40), db.ForeignKey('user.uuid'))
    content = db.Column(db.String(40), db.ForeignKey('content.uuid'))
    format = db.Column(db.String(40), db.ForeignKey('format.uuid'))
    schedule = db.relationship('EventSchedule', backref='related_event', lazy='dynamic')

    
    def __repr__(self):
        return '<Event %r>' %(self.topic)


    def __init__(self, topic, description, min_attendance, max_attendance, speaker, create_by, content, format, schedule=[]):
        self.uuid = str(uuid.uuid1())
        self.topic = topic
        self.description = description
        self.min_attendance = min_attendance
        self.max_attendance = max_attendance
        self.speaker = speaker
        self.create_by = create_by
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
        self.status = 0
        #self.content = content
        #self.format = format
        self.schedule = schedule
        input_content = db.session.query(Content).filter(Content.name == content).first()
        input_format = db.session.query(Format).filter(Format.name == format).first()
        input_content.events.append(self)
        input_format.events.append(self)


    def is_created_by(self, user_uuid):
        if self.create_by == user_uuid:
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
    name = db.Column(db.String(10), index=True, unique=True)
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
    create_by = db.Column(db.String(20))
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
    create_by = db.Column(db.String(20))
    r_type = db.Column(db.String(40), db.ForeignKey('resource_type.uuid'))
    schedules = db.relationship('EventSchedule', backref='assigned_resource', lazy='dynamic')


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
    event = db.Column(db.String(40), db.ForeignKey('event.uuid'))
    start_date = db.Column(db.Date, default='1970-01-01')
    time_from = db.Column(db.Time, nullable=True)
    time_to = db.Column(db.Time, nullable=True)
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    create_by = db.Column(db.String(20))
    resource = db.Column(db.String(40), db.ForeignKey('resource.uuid'))


    def __repr__(self):
        return '<EventSchedule %r>' %(self.topic)


    def __init__(self, start_date, time_from, time_to, event, resource, create_by):
        self.uuid = str(uuid.uuid1())
        self.start_date = start_date
        self.time_from = time_from
        self.time_to = time_to
        self.event = event
        self.resource = resource
        self.create_by = create_by
        self.create_time = time.strftime("%H:%M:%S")
        self.create_date = time.strftime("%Y/%m/%d")
