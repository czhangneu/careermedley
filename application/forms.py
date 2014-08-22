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

class ApplicationForm(Form):
    apply_date = StringField('Apply Date', [InputRequired()])
    resume_version = StringField('Resume')
    cv_version = StringField('CV')
    username_on_website = StringField('Username', [InputRequired()])
    password_on_website = StringField('Password', [InputRequired()])
    submit = SubmitField('Submit')

class EmployerForm(Form):
    employer_name = StringField('Employer Name', [InputRequired()])
    num_ratings = StringField('Ratings', [InputRequired()])
    score = StringField('Score', [InputRequired()])
    ceo_name = StringField('CEO name', [InputRequired()])
    num_ceo_review = StringField('CEO review', [InputRequired()])
    ceo_approval = StringField('CEO Approval')
    submit = SubmitField('Submit')