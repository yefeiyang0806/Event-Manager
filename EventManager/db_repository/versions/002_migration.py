from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
roles_menus = Table('roles_menus', pre_meta,
    Column('role_id', VARCHAR(length=40)),
    Column('menu_id', VARCHAR(length=40)),
)

role_menu = Table('role_menu', post_meta,
    Column('uuid', String(length=40), primary_key=True, nullable=False),
    Column('role_id', String(length=40), primary_key=True, nullable=False),
    Column('menu_id', String(length=40), primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['roles_menus'].drop()
    post_meta.tables['role_menu'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['roles_menus'].create()
    post_meta.tables['role_menu'].drop()
