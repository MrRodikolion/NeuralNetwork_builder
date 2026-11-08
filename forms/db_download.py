from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class DataBaseProjectGen(FlaskForm):
    img_size_x = IntegerField('Size', validators=[DataRequired(), NumberRange(min=1, max=4096)], default=416)
    img_size_y = IntegerField('Size', validators=[DataRequired(), NumberRange(min=1, max=4096)], default=416)
    is_add_gray = BooleanField('Gray Scale')
    is_add_blur = BooleanField('Blur')
    is_add_noise = BooleanField('Noise')
    submit = SubmitField('Generate/Download')
