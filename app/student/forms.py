from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField


class UserForm(FlaskForm):
    id = StringField('ID', [validators.DataRequired()])
    firstname = StringField('First Name', [validators.DataRequired(), validators.Length(min=1, max=30)])
    lastname = StringField('Last Name', [validators.DataRequired(), validators.Length(min=1, max=30)])
    course = StringField('Course', [validators.DataRequired(), validators.Length(min=1, max=30)])
    year = StringField('Year', [validators.DataRequired(), validators.Length(min=1, max=30)])
    gender = StringField('Gender', [validators.DataRequired(), validators.Length(min=1, max=30)])
    submit = SubmitField("Submit")
