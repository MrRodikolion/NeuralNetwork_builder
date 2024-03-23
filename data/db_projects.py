import sqlalchemy as sa
from sqlalchemy import orm
from flask_login.mixins import UserMixin
from .db_session import SqlAlchemyBase


class DataBaseProject(SqlAlchemyBase):
    __tablename__ = 'db_projects'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    name = sa.Column(sa.String)
    href = sa.Column(sa.String)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship('User')

    images = orm.relationship('Image', back_populates='project')


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    data = sa.Column(sa.BLOB)

    project_id = sa.Column(sa.Integer, sa.ForeignKey('db_projects.id'))
    project = orm.relationship('DataBaseProject')
