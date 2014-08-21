#!/usr/bin/python
__author__ = 'onyekaigabari'

from flask import render_template, flash, \
    redirect, g, url_for, request, session, send_from_directory
from application import app, lm, db, oid

from forms import LoginForm, JobSearchForm,\
    ProfileForm, ApplicationForm, EmployerForm

from job_search import ProcessJobSearch

from models import User, Position, Account, Employer,\
    Document, Application, ROLE_USER
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

def set_upload_dir(nickname):
        g.user.nickname = nickname
        g.user.upload_dir = os.path.join(basedir, nickname, 'files/')

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
        g.user.nickname = nickname

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

@app.route('/user/<nickname>/<jobkey>/proxy')
@login_required
def application_proxy(nickname, jobkey):
    print "+++++ reroute from proxy application ++++"
    return redirect(url_for('save_applications', nickname=nickname, jobkey=jobkey))

# *****************************************************************
# Page: /user/<nickname>/<jobkey>/apply
# Method: save_application
# Description: Saves an application into the database
# Params: nickname, jobkey
# *****************************************************************
@app.route('/user/<nickname>/<jobkey>/apply', methods=['GET', 'POST'])
@login_required
def save_applications(nickname, jobkey):
    print "====== got into save_applications jobkey: " , jobkey
    set_upload_dir(nickname)
    form = ApplicationForm()
    if request.method == 'POST' and form.validate_on_submit():
        apply_date = form.apply_date.data
        resume = form.resume_version.data
        cv = form.cv_version.data
        username = form.username_on_website.data
        password = form.password_on_website.data
        user = User.query.filter_by(nickname=nickname).first()
        position = Position.query.filter_by(jobkey=jobkey).first()
        if user is not None and position is not None:
            application = Application(id=user.id, jobkey=position.jobkey,
                                      apply_date=apply_date, resume=resume, cv=cv)
            db.session.add(application)
            db.session.commit()
        else :
            flash(" We couldn't save the position.")
        return redirect(url_for('application_list', nickname=nickname))

    print "documents available: ", os.listdir(g.user.upload_dir), " path is: ", g.user.upload_dir
    documents = os.listdir(g.user.upload_dir)
    return render_template('save_applications.html',
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
#@app.route('/user/<nickname>/applications', methods=['GET', 'POST'])
@login_required
def list_applications(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    applications = Application.query.filter_by(id=user.id).all()
    print " applications: ", applications
    positions = []
    for application in applications:
        positions.append(Position.query.filter_by(jobkey=application.jobkey).first())
    return render_template('list_applications.html', user=g.user,
                           positions=positions)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# *****************************************************************
# Page: /user/<nickname>/upload
# Method: upload
# Description: uploads a file to the application
# Params: nickname
# *****************************************************************
@app.route('/user/<nickname>/upload', methods=['GET', 'POST'])
@login_required
def upload(nickname):
    set_upload_dir(nickname)
    user = g.user
    #print "uploaded folder is: " , user.upload_dir
    if not os.path.exists(user.upload_dir):
        os.makedirs(user.upload_dir)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(user.upload_dir, filename)
            file.save(file_path)
            print "file requested: ", file, " file is: ", file_path

            # save file to database if not currently saved
            doc = Document.query.filter_by(doc_name=file.filename).first()
            account = Account.query.filter_by(id=user.id).first()
            print " doc: %s, account: %s" % (doc, account.id)
            if doc is None:
                doc = Document(id=account.id, doc_name=filename, doc_path=file_path)
                db.session.add(doc)
                db.session.commit()
            else:
                print " previously saved!!!"
    return render_template('upload.html', user=user, upload_folder_files=os.listdir(user.upload_dir))

@app.route('/user/<nickname>/upload/<filename>')
def uploaded_file(filename, nickname):
    set_upload_dir(nickname)
    user = g.user
    return send_from_directory(user.upload_dir, filename)

@app.route('/user/<nickname>/favorite_employers', methods=['GET', 'POST'])
@app.route('/user/<nickname>/favorite_employers/<int:page>', methods=['GET', 'POST'])
@login_required
def favorite_employers(nickname, page=1):
    user = g.user
    form = EmployerForm()
    employers = Employer.query.paginate(page, 10, False)
    return render_template('favorite_employers.html',
                           title=nickname,
                           employers = employers,
                           user=user, form=form)
