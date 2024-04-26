import sqlalchemy as sa
from sqlalchemy import orm
from flask_login.mixins import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    username = sa.Column(sa.String, nullable=True, unique=True)
    email = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String)

    projects = orm.relationship('DataBaseProject', back_populates='user')

    def check_password(self, password):
        return password == self.hashed_password