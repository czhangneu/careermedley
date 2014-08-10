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

# class LoginForm(Form):
#     username = StringField('Username', [InputRequired()])
#     password = PasswordField('Password', [InputRequired()])
#     submit = SubmitField('Log In')
