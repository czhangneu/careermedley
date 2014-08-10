import os
from flask import Flask
from flask_bootstrap3 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_openid import OpenID
from config import basedir
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.session_protection = 'strong'
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


from application import views, models


