from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class AddtaskForm(FlaskForm):
    name = StringField("Task name:")
    description = TextAreaField("Description:")
    submit = SubmitField("Add")