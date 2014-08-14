
__author__ = 'onyekaigabari'

from macros import SHORT_STR_LEN, MEDIUM_STR_LEN, LONG_STR_LEN
from application import db, UserMixin

ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    #username = db.Column(db.String(50), index=True, unique=True)
    #password = db.Column(db.String(50), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return 'User %r>' % (self.username)

class Account(db.Model):
   __tablename__ = 'Account'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer)
   firstname = db.Column(db.String(100))
   lastname = db.Column(db.String(100))
   city = db.Column(db.String(100))
   state = db.Column(db.String(100))
   country = db.Column(db.String(100))
   zipcode = db.Column(db.Integer)
   major = db.Column(db.String(100))
   degree = db.Column(db.String(100))
   #user = db.relationship('User',
   #     backref=db.backref('account', lazy='joined'), lazy='dynamic')
   #user = db.relationship("User", backref=db.backref("account", lazy='joined', uselist=False))

   def __init__(self, user_id, firstname=None, lastname=None, city=None,
                state = None, country=None, zipcode = 11111, major=None, degree=None):
       self.user_id = user_id
       self.firstname = firstname
       self.lastname = lastname
       self.city = city
       self.state = state
       self.country = country
       self.zipcode = zipcode
       self.major = major
       self.degree = degree

   def __repr__(self):
       return 'Accout %r>' % (self.firstname)


class Position(db.Model):
   positionid = db.Column(db.Integer, primary_key=True)
   company    = db.Column(db.String(SHORT_STR_LEN))
   jobtitle   = db.Column(db.String(SHORT_STR_LEN))
   city       = db.Column(db.String(SHORT_STR_LEN))
   state      = db.Column(db.String(SHORT_STR_LEN))
   short_desc = db.Column(db.String(LONG_STR_LEN))
   post_date  = db.Column(db.DateTime)
   url        = db.Column(db.String(MEDIUM_STR_LEN))
   jobkey     = db.Column(db.String(SHORT_STR_LEN), unique = True)
   expired    = db.Column(db.Boolean)
   role       = db.Column(db.SmallInteger, default=ROLE_USER)

   def __init__(self, company, jobtitle, city, state,
                short_desc, post_date, url, jobkey, expired):
       self.company = company
       self.jobtitle = jobtitle
       self.city = city
       self.state = state
       self.short_desc = short_desc
       self.post_date = post_date
       self.url = url
       self.jobkey = jobkey
       self.expired = expired

   def __repr__(self):
       return '<Position %r>' % self.jobtitle
