from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class DataBaseProjectCreateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    data_type = RadioField('Data type', choices=[('img', 'Imgages')], validators=[DataRequired()])
    submit = SubmitField('Create')


class NeuralNetworkProjectCreateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    submit = SubmitField('Create')
