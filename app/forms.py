from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class createPrisonerForm(Form):
    name = StringField('name', validators=[DataRequired()])

