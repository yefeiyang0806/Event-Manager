from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', post_meta,
    Column('uuid', String(length=40), primary_key=True, nullable=False),
    Column('menu', String(length=40)),
    Column('menu_path', String(length=40)),
)

role = Table('role', post_meta,
    Column('uuid', String(length=40), primary_key=True, nullable=False),
    Column('rolename', String(length=20)),
    Column('description', String(length=40)),
    Column('create_date', Date),
    Column('create_time', Time),
    Column('create_by', String(length=40)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].create()
    post_meta.tables['role'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].drop()
    post_meta.tables['role'].drop()
