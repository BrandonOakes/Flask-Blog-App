from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo

import models


def email_exists(form, field):
    """checks to see if email address already exist in database prior
    registration
    """
    if models.User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exist.")


class RegisterForm(Form):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo('password2', message='Passwords need to match')
        ])
    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired()
        ])


class LoginForm(Form):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])


class NewEntry(Form):
    """Web form for user to submit new entry"""

    title = StringField(
            "Title",
            validators=[
            DataRequired()
            ]
        )
    date = DateField(
            "Date (mm/dd/year)",
            format='%m/%d/%Y',
            validators=[
            DataRequired()
            ]
    )
    time = StringField(
            'Time Spent',
            validators=[
            DataRequired()
            ]
    )
    learned = TextAreaField(
            'What I Learned',
            validators=[
            DataRequired()
            ]
    )
    resources = TextAreaField(
            'Resources to Remember',
            validators=[
            DataRequired()
            ]
    )


class EditEntry(Form):
    """Web form for user to submit new entry"""

    title = StringField(
            "Title",
            validators=[
            DataRequired()
            ]
        )
    date = DateField(
            "Date (mm/dd/year)",
            format='%m/%d/%Y',
            validators=[
            DataRequired()
            ]
    )
    time = StringField(
            'Time Spent',
            validators=[
            DataRequired()
            ]
    )
    learned = TextAreaField(
            'What I Learned',
            validators=[
            DataRequired()
            ]
    )
    resources = TextAreaField(
            'Resources to Remember',
            validators=[
            DataRequired()
            ]
    )
