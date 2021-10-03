from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.fields.core import RadioField, SelectField


class UserForm(FlaskForm):
    id = StringField('ID', [validators.DataRequired()])
    firstname = StringField('First Name', [validators.DataRequired(), validators.Length(min=1, max=30)])
    lastname = StringField('Last Name', [validators.DataRequired(), validators.Length(min=1, max=30)])
    course = SelectField('Course', choices=[])
    year = SelectField('Year', choices=[('1st','1st'),('2nd','2nd'),('3rd','3rd'),('4th','4th')])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'),('Other','Other'),('Prefer not to say','Prefer not to say')])
    submit = SubmitField("Submit")

    def __init__(self, id = None, firstname = None, lastname = None, course = None, year = None, gender = None):
        super().__init__()
        self.process()
        if id:
            self.id.default = id
            self.firstname.default = firstname
            self.lastname.default = lastname
            self.course.default = course
            self.year.default = year
            self.gender.default = gender
            self.process()