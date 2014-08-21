#!/usr/bin/python
__author__ = 'onyekaigabari'

from flask import render_template, flash, \
    redirect, g, url_for, request, session, send_from_directory
from application import app, lm, db, oid
from forms import LoginForm, JobSearchForm, ProfileForm, ApplicationForm
from job_search import ProcessJobSearch
from models import User, Position, Account, ROLE_USER
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from config import ALLOWED_EXTENSIONS

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# run this before the view is created
@app.before_request
def before_request():
    g.user = current_user
    g.user.upload_dir = os.path.join(basedir, g.user.nickname, 'files/')


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
# Method: delete
# Description: displays the marked jobs from the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/bookmarked/<jobkey>', methods=['GET', 'POST'])
@login_required
def delete(nickname, jobkey):
    print "====yay delete got here, nickname: %s, jobkey:%s" % (nickname, jobkey)
    user = g.user
    position = Position.query.filter_by(jobkey=jobkey).first()
    if position is None:
        print(" couldn't delete job with jobkey: ", jobkey)
    else:
        # delete marked position
        account = Account.query.filter_by(id=g.user.id).first()
        position.unmark_position(account)
        db.session.add(position)
        db.session.delete(position)
        db.session.commit()
    return redirect(url_for('bookmarked', nickname=nickname))

# *****************************************************************
# Method: bookmarked
# Description: displays the marked jobs from the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/bookmarked', methods=['GET', 'POST'])
@login_required
def bookmarked(nickname):
    account = Account.query.filter_by(id=g.user.id).first()
    marked_positions = account.get_all_marked_positions()
    print "-----marked positions for Account: ", marked_positions

    return render_template('marked_jobs.html',
                           user=g.user,
                           positions=marked_positions)

# *****************************************************************
# Page: /user/<nickname>/<jobkey>
# Method: save_job
# Description: Saves a job into the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/<jobkey>', methods=['GET', 'POST'])
@login_required
def save_job(nickname, jobkey):
    getJob = ProcessJobSearch()
    job = getJob.search_by_jobkeys(jobkey)
    job_data = job[0]
    print "====yay got here, nickname: %s, jobkey: %s, job: %s" % (nickname, jobkey, job)
    print(job_data['date'])

    position = Position.query.filter_by(jobkey=job_data['jobkey']).first()
    if position is None:
        dt = datetime.strptime(job_data['date'], "%a, %d %b %Y %H:%M:%S %Z" )
        print(" time object is: %s" % dt)
        position = Position(jobkey=job_data['jobkey'], company=job_data['company'],
                            jobtitle=job_data['jobtitle'], city=job_data['city'],
                            state=job_data['state'], snippet=job_data['snippet'],
                            post_date=dt, url=job_data['url'],
                            expired=job_data['expired'])
        print "new position, adding to database: %s", position
        db.session.add(position)
        db.session.commit()

        # insert into marked position table
        account = Account.query.filter_by(id=g.user.id).first()
        position.mark_position(account)
        db.session.add(position)
        db.session.commit()

    else:
        print " this is an old position"

    return redirect(url_for('user', nickname=nickname))

# *****************************************************************
# Page: /user/<nickname>
# Method: user
# Description: This will display the profile page if the user hasn't
# created an account, or the user's main
# page.
# Params: nickname
# *****************************************************************
@app.route('/user/<nickname>/applications', methods=['GET', 'POST'])
@login_required
def applications(nickname):
    form = ApplicationForm()
    if request.method == 'POST' and form.validate_on_submit():
        apply_date = form.apply_date.data
        resume = form.resume_version.data
        cv = form.cv_version.data
        username = form.username_on_website.data
        password = form.password_on_website.data
        print "values received: ", apply_date, resume, cv, username, password
    #print "documents available: ", os.listdir(g.user.upload_dir), " path is: ", g.user.upload_dir
    documents = os.listdir(g.user.upload_dir)
    return render_template('applications.html',
                           nickname=nickname,
                           user=g.user, form=form,
                           documents=documents)

# *****************************************************************
# Page: /user/<nickname>
# Method: user
# Description: This will display the profile page if the user hasn't
# created an account, or the user's main
# page.
# Params: nickname
# *****************************************************************
@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user(nickname):
    print(request.args.get("jobkey"))
    user = g.user
    account = Account.query.filter_by(id=user.id).first()
    print "are we here? account: %s" % account
    if account is None:
        form = ProfileForm()
        if request.method == 'POST' and form.validate_on_submit():
            print "yes we got here....user.id: %s, user.email: %s" % (user.id, user.email)
            firstname = form.firstname.data
            lastname = form.lastname.data
            city = form.city.data
            state = form.state.data
            country = form.country.data
            zipcode = form.zipcode.data
            major = form.major.data
            degree = form.degree.data
            account = Account(id=user.id, firstname=firstname, lastname=lastname,
                        city=city, state=state, country=country, zipcode=zipcode,
                        major=major, degree=degree)
            print " account: %s" % account
            db.session.add(account)
            db.session.commit()
            jobForm = JobSearchForm()
            return render_template('user.html',
                                   nickname=nickname,
                                   user=user,
                                   form=jobForm)
        return render_template('profile.html', nickname=nickname,
                               user=user,
                               form=form)
    else:
        jobForm = JobSearchForm()
        if request.method == 'POST':
            if jobForm.validate_on_submit():
                getJobs = ProcessJobSearch()
                jobs = getJobs.job_search(jobForm.job.data, jobForm.location.data)
                for i in range(len(jobs)):
                    print "range (%d: %s)" % (i, jobs[i])
                    print '*' * 100
                return render_template('user.html',
                                       title='CareerMedley',
                                       form=jobForm, user=user, jobs=jobs)
    return render_template('user.html',
                           title=nickname,
                           form=jobForm,
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
    #print "uploaded folder is: " , user.upload_dir
    if not os.path.exists(user.upload_dir):
        os.makedirs(user.upload_dir)
    if request.method == 'POST':
        file = request.files['file']
        print "file requested: ", file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(user.upload_dir, filename))

    return render_template('upload.html', user=user, upload_folder_files=os.listdir(user.upload_dir))

@app.route('/user/<nickname>/upload/<filename>')
def uploaded_file(filename, nickname):
    user = g.user
    return send_from_directory(user.upload_dir, filename)
