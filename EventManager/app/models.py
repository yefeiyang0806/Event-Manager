from app import db
import time, uuid

class User(db.Model):
    uuid = db.Column(db.String(32), primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    create_date = db.Column(db.Date)
    create_time = db.Column(db.Time)
    events = db.relationship('Event', backref='author', lazy='dynamic')
    status = db.Column(db.Integer, default=0)
    active_code = db.Column(db.String(4))


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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.String(360))
    min_attendance = db.Column(db.Integer)
    max_attendance = db.Column(db.Integer)
    location = db.Column(db.String(240))
    host = db.Column(db.String(120))
    status = db.Column(db.String(30), default="unapproved")
    start_date = db.Column(db.Date, default='1970-01-01')
    duration = db.Column(db.Integer)
    user_id = db.Column(db.String(128), db.ForeignKey('user.uuid'))

    
    def __repr__(self):
        return '<Event %r>' %(self.topic)


    def __init__(self, topic, description, min_attendance, max_attendance, location, host, start_date, duration, user_id):
        self.topic = topic
        self.description = description
        self.min_attendance = min_attendance
        self.max_attendance = max_attendance
        self.location = location
        self.host = host
        self.user_id = user_id
        self.status = 'unapproved'
        self.start_date = start_date
        self.duration = duration


    def is_created_by(self, user_uuid):
        if self.user_id == user_uuid:
            return True

        else:
            return False
