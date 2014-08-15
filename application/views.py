#!/usr/bin/python
__author__ = 'onyekaigabari'

from flask import render_template, flash, redirect, g, url_for, request, session
from application import app, lm, db, oid
from forms import LoginForm, JobSearchForm, ProfileForm
from job_search import ProcessJobSearch
from models import User, Position, ROLE_USER
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# run this before the view is created
@app.before_request
def before_request():
    g.user = current_user


# Handles user search request
@app.route('/', methods=['GET', 'POST'])
def main_page():
    user = g.user
    form = JobSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            getJobs = ProcessJobSearch()
            jobs = getJobs.job_search(form.job.data, form.location.data)
            for i in range(len(jobs)):
                print "range (%d: %s)" % (i, jobs[i])
                print '*' * 100
            return render_template('main_page.html',
                                   user=user,
                                   title='CareerMedley',
                                   form=form, jobs=jobs)
        else:
            print " form isn't valid..."
    return render_template('main_page.html',
                           user=user,
                           title='CareerMedley', form=form)


# Handles user login request
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('user', nickname=g.user.nickname))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('user', user.nickname))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# *****************************************************************
# Method: bookmarked
# Description: displays the marked jobs from the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/bookmarked/<jobkey>', methods=['GET', 'POST'])
@login_required
def bookmarked(nickname, jobkey):
    #print "====yay bookmarked got here, nickname: %s, jobkey: %s" % (nickname, jobkey)
    user = g.user
    positions = Position.query.all()
    if(jobkey != True):
        position = Position.query.filter_by(jobkey=jobkey).first()
        if position is not None:
            db.session.delete(position)
            db.session.commit()
            positions = Position.query.all()
    return render_template('marked_jobs.html',
                           user=user,
                           positions=positions)

# *****************************************************************
# Page: /user/<nickname>/<jobkey>
# Method: save_job
# Description: Saves a job into the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/<jobkey>', methods=['GET', 'POST'])
@login_required
def save_job(nickname, jobkey):
    print "====yay got here, nickname: %s, jobkey: %s" % (nickname, jobkey)
    getJob = ProcessJobSearch()
    job = getJob.search_by_jobkeys(jobkey)
    job_data = job[0]
    print(job_data['date'])
    position = Position.query.filter_by(jobkey=job_data['jobkey']).first()
    if position is None:
        print "new position, adding to database"
        dt = datetime.strptime(job_data['date'], "%a, %d %b %Y %H:%M:%S %Z" )
        print(" time object is: %s" % dt)
        position = Position(jobkey= job_data['jobkey'], jobtitle=job_data['jobtitle'],
                            company=job_data['company'], city=job_data['city'],
                            state=job_data['state'], url=job_data['url'],
                            post_date=dt, short_desc=job_data['snippet'],
                            expired=job_data['expired'])

        db.session.add(position)
        db.session.commit()
    else:
        print " this is an old position"
    return redirect(url_for('user', nickname=nickname))

@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user(nickname):
    print "shouldn't be here"
    print(request.args.get("jobkey"))
    user = g.user
    form = JobSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            getJobs = ProcessJobSearch()
            jobs = getJobs.job_search(form.job.data, form.location.data)
            for i in range(len(jobs)):
                print "range (%d: %s)" % (i, jobs[i])
                print '*' * 100
            return render_template('user.html',
                                   title='CareerMedley',
                                   form=form, user=user, jobs=jobs)
    return render_template('user.html',
                           title=nickname,
                           form=form,
                           user=user)

@app.route('/user/<nickname>/profile', methods=['GET', 'POST'])
@login_required
def profile(nickname):
    user = g.user
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            city = form.city.data
            state = form.state.data
            country = form.country.data
            zipcode = form.zipcode.data
            major = form.major.data
            degree = form.degree.data

    return render_template('profile.html',
                           title=nickname,
                           form=form,
                           user=user)

import os
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# UPLOAD_FOLDER = os.path.join(basedir, 'files/')
# print UPLOAD_FOLDER
# if not os.path.exists(UPLOAD_FOLDER):
#     os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
#
#
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
@app.route('/user/<nickname>/upload', methods=['GET', 'POST'])
@login_required
def upload(nickname):
    user = g.user
    UPLOAD_FOLDER_part1 = os.path.join(basedir, user.nickname)
    UPLOAD_FOLDER_part2 = os.path.join(basedir, user.nickname, 'files/')
    print UPLOAD_FOLDER_part1
    print UPLOAD_FOLDER_part2
    if not os.path.exists(UPLOAD_FOLDER_part1):
        os.mkdir(UPLOAD_FOLDER_part1)
    if not os.path.exists(UPLOAD_FOLDER_part2):
        os.mkdir(UPLOAD_FOLDER_part2)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(UPLOAD_FOLDER_part2, filename))
            #return redirect(url_for('upload'))
            return render_template('upload.html', user=user, upload_folder_files=os.listdir(UPLOAD_FOLDER_part2,))
    #return render_template('upload.html', user=user, files=os.listdir(app.config['UPLOAD_FOLDER'],))
    return render_template('upload.html', user=user, upload_folder_files=os.listdir(UPLOAD_FOLDER_part2,))

#
from flask import send_from_directory

@app.route('/user/<nickname>/upload/<filename>')
def uploaded_file(filename, nickname):
    UPLOAD_FOLDER_part2 = os.path.join(basedir, g.user.nickname, 'files/')

    return send_from_directory(UPLOAD_FOLDER_part2,
                               filename)
