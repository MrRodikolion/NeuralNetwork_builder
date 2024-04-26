from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class DeleteProjectForm(FlaskForm):
    submit = SubmitField('Delete')
