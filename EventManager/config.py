import os

CSRF_ENABLED = True
SECRET_KEY = 'feeeeeiyang'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootadmin@localhost:3306/event_manager'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = '18616374350@163.com'
MAIL_PASSWORD = 'ltqqjrgysbpyerow'

ADMINS = ['18616374350@163.com']