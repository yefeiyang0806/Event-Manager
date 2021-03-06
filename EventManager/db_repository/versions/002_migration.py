from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', post_meta,
    Column('uuid', String(length=40), primary_key=True, nullable=False),
    Column('event_id', String(length=20)),
    Column('name', String(length=60)),
    Column('description', String(length=400)),
    Column('start_date', Date),
    Column('end_date', Date),
    Column('email_template', String(length=200)),
    Column('reserve_1', String(length=255)),
    Column('reserve_2', String(length=255)),
    Column('create_date', Date),
    Column('create_time', Time),
    Column('create_by', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['name'].drop()
