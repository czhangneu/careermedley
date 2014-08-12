__author__ = 'onyekaigabari'

from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired

# define forms
class JobSearchForm(Form):
    job = StringField('job', [InputRequired()])
    location = StringField('location', [InputRequired()])
    search = SubmitField('Search')

class LoginForm(Form):
    openid = StringField('openid', validators = [InputRequired()])
    remember_me = BooleanField('Remember me', default = False)

class ProfileForm(Form):
     firstname = StringField('FirstName', [InputRequired()])
     lastname = StringField('LastName', [InputRequired()])
     city = StringField('City', [InputRequired()])
     state = StringField('State', [InputRequired()])
     country = StringField('Country', [InputRequired()])
     zipcode = StringField('Zipcode', [InputRequired()])
     major = StringField('Major', [InputRequired()])
     degree = StringField('Degree', [InputRequired()])
     submit = SubmitField('Submit')
