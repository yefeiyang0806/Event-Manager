from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER(display_width=11), primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=120)),
    Column('first_name', VARCHAR(length=10)),
    Column('last_name', VARCHAR(length=10)),
    Column('create_date', DATE),
    Column('create_time', TIME),
    Column('status', INTEGER(display_width=11)),
    Column('active_code', VARCHAR(length=4)),
)

user = Table('user', post_meta,
    Column('uuid', String(length=128), primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('first_name', String(length=10)),
    Column('last_name', String(length=10)),
    Column('create_date', Date),
    Column('create_time', Time),
    Column('status', Integer, default=ColumnDefault(0)),
    Column('active_code', String(length=4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['id'].drop()
    post_meta.tables['user'].columns['uuid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['id'].create()
    post_meta.tables['user'].columns['uuid'].drop()
