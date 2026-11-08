from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Regexp


class DataBaseProjectCreateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired(), Regexp(r'^[^/?#]+$', message='Project name cannot contain /, ? or #.')])
    data_type = RadioField('Data type', choices=[('img', 'Imgages')], validators=[DataRequired()])
    submit = SubmitField('Create')


class NeuralNetworkProjectCreateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired(), Regexp(r'^[^/?#]+$', message='Project name cannot contain /, ? or #.')])
    submit = SubmitField('Create')
