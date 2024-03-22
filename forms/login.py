from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    mail = StringField('email', validators=[DataRequired()])

    password = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('Log-in')
