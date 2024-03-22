from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SinginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    mail = StringField('email', validators=[DataRequired()])

    password = PasswordField('password', validators=[DataRequired()])
    conf_password = PasswordField('conf_password', validators=[DataRequired()])

    submit = SubmitField('Sing-in')
