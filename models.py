from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

import datetime

DATABASE = SqliteDatabase('post.db')


class User(UserMixin, Model):
    """Stores user login and password"""
    email = CharField(unique=True)
    password = CharField()

    @classmethod
    def create_user(cls, email, password):
        """class method that creates user"""
        try:
            with DATABASE.transaction():
                cls.create(
                email=email,
                password=generate_password_hash(password),
                )
        except IntegrityError:
            raise ValueError("Sorry, this user already exist")

    class Meta():
        """class Meta"""

        database = DATABASE


class Post(Model):
    """creates journal entry instance to be stored in database"""

    user_id = ForeignKeyField(User, backref="post")
    title = CharField(unique=True)
    date = DateField(default=datetime.datetime.now)
    time = CharField()
    learned = TextField()
    resources = TextField()

    class Meta:
        """Meta class"""

        database = DATABASE


def initialize():
    """initiates communication to database"""
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
