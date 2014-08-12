#!/usr/bin/python
__author__ = 'onyekaigabari'

from flask import render_template, flash, redirect, g, url_for, request, session
from application import app, lm, db, oid
from forms import LoginForm, JobSearchForm, ProfileForm
from job_search import ProcessJobSearch
from models import User, ROLE_USER, ROLE_ADMIN
from flask_login import login_user, logout_user, login_required, current_user
import json


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
    form = JobSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            getJobs = ProcessJobSearch()
            jobs = getJobs.job_search(form.job.data, form.location.data)
            for i in range(len(jobs)):
                print "range (%d: %s)" % (i, jobs[i])
                print '*' * 100
            return render_template('main_page.html',
                                   title='CareerMedley',
                                   form=form, jobs=jobs)
        else:
            print " form isn't valid..."
    return render_template('main_page.html',
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

@app.route('/index')
@login_required
def index():
    render_template('index.html')

@app.route('/user/<nickname>/<jobkey>', methods=['GET', 'POST'])
@login_required
def save_job(nickname, jobkey):
    print "====yay got here, nickname: %s, jobkey: %s" % (nickname, jobkey)
    print(request)
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
