#!/usr/bin/python

__author__ = 'onyekaigabari'

import os

# Set Cross Site Request Forgery (CSRF) to true.
# This makes our app more secure
CSRF_ENABLED = True

# Needed when CSRF is enabled. Creates a cryptographic token for
# validating forms .
SECRET_KEY = 'career-medley-rocks!'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
print "====basedir is: " + basedir

PUBLISHER = '5950869068484812'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    #{ 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]