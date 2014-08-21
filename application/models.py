__author__ = 'onyekaigabari'


from hashlib import md5
from application import app, db, UserMixin
import flask_whooshalchemy as whooshalchemy
from macros import SHORT_STR_LEN, MEDIUM_STR_LEN, LONG_STR_LEN

ROLE_USER = 0
ROLE_ADMIN = 1

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(SHORT_STR_LEN), unique = True)
    email = db.Column(db.String(MEDIUM_STR_LEN), index = True, unique = True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def avatar(self, size):
        print "show avatar"
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return 'User %r>' % (self.username)

class Account(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstname = db.Column(db.String(MEDIUM_STR_LEN))
    lastname = db.Column(db.String(MEDIUM_STR_LEN))
    city = db.Column(db.String(MEDIUM_STR_LEN))
    state = db.Column(db.String(MEDIUM_STR_LEN))
    country = db.Column(db.String(MEDIUM_STR_LEN))
    zipcode = db.Column(db.Integer)
    major = db.Column(db.String(MEDIUM_STR_LEN))
    degree = db.Column(db.String(MEDIUM_STR_LEN))
    # user-account: one-to-one map
    user = db.relationship("User", backref=db.backref("account", lazy='joined', uselist=False))

    def __init__(self, id, firstname, lastname, city,
                 state, country, zipcode, major, degree):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode
        self.major = major
        self.degree = degree

    def __repr__(self):
        return 'Account %r>' % (self.firstname)

    def get_all_marked_positions(self):
        return self.marked_positions.filter(MarkedPosition.c.account_id == self.id)

MarkedPosition = db.Table('marked_positions',
                          db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                          db.Column('position_id', db.Integer, db.ForeignKey('position.jobkey')),
                          db.Column('marked', db.Boolean))

class Position(db.Model):
    __searchable__ = ['jobtitle']  # the field that will be created index

    jobkey = db.Column(db.String, primary_key=True, unique=True)
    company = db.Column(db.String(MEDIUM_STR_LEN))
    jobtitle = db.Column(db.String(MEDIUM_STR_LEN))
    city = db.Column(db.String(MEDIUM_STR_LEN))
    state = db.Column(db.String(SHORT_STR_LEN))
    snippet = db.Column(db.String(LONG_STR_LEN))
    post_date = db.Column(db.DateTime)
    url = db.Column(db.String(LONG_STR_LEN))
    expired = db.Column(db.Boolean)
    user_accounts = db.relationship('Account', secondary=MarkedPosition,
                                    backref=db.backref('marked_positions', lazy='dynamic'),
                                    lazy = 'dynamic')

    def __init__(self, jobkey, company, jobtitle, city, state,
                 snippet, post_date, url, expired):
        self.jobkey = jobkey
        self.company = company
        self.jobtitle = jobtitle
        self.city = city
        self.state = state
        self.snippet = snippet
        self.post_date = post_date
        self.url = url
        self.expired = expired

    def __repr__(self):
        return '<Position jobtitle: %r, jobkey: %r >' % (self.jobtitle, self.jobkey)

    def mark_position(self, account):
        if not self.is_marked_by_account_owner(account):
            self.user_accounts.append(account)
            return self

    def unmark_position(self, account):
        if self.is_marked_by_account_owner(account):
            self.user_accounts.remove(account)
            return self

    def is_marked_by_account_owner(self, account):
        return self.user_accounts.filter(MarkedPosition.c.account_id == account.id).count() > 0

class Application(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    jobkey = db.Column(db.String, db.ForeignKey('position.jobkey'), primary_key=True)
    apply_date = db.Column(db.DateTime)
    resume = db.Column(db.String(LONG_STR_LEN))
    cv = db.Column(db.String(LONG_STR_LEN))

    user = db.relationship('User', backref=db.backref('applications', lazy='dynamic'))
    position = db.relationship('Position', backref=db.backref('applications', lazy='dynamic'))

    def __init__(self, id, jobkey, apply_date, resume, cv):
        self.id = id
        self.jobkey = jobkey
        self.apply_date = apply_date
        self.resume = resume
        self.cv = cv

    def __repr__(self):
        return '<Application %r>' % self.accountid

class Document(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    doc_name = db.Column(db.String(LONG_STR_LEN), unique=True)
    doc_path = db.Column(db.String(LONG_STR_LEN), unique=True)

    user = db.relationship('User', backref=db.backref('documents', lazy='dynamic'))

    def __init__(self, id, doc_name, doc_path):
        self.id = id
        self.doc_name = doc_name
        self.doc_path = doc_path

    def __repr__(self):
        return '<Account: %s, Document %s>' % (self.id, self.doc_name)

class Employer(db.Model):
    employer_name = db.Column(db.String(MEDIUM_STR_LEN), primary_key=True)
    num_ratings = db.Column(db.Integer)
    score = db.Column(db.String)
    ceo_name = db.Column(db.String(MEDIUM_STR_LEN))
    num_ceo_reviews = db.Column(db.Integer)
    # ceo_approval rate e.g. 98 -> 98%
    ceo_approval = db.Column(db.Integer)

    def __init__(self, employer_name, num_ratings, score, ceo_name,
                 num_ceo_reviews, ceo_approval):
        self.employer_name = employer_name
        self.num_ratings = num_ratings
        self.score = score
        self.ceo_name = ceo_name
        self.num_ceo_reviews = num_ceo_reviews
        self.ceo_approval = ceo_approval

    def __repr__(self):
        return '<Employer: %s>' % (self.employer_name)

# ---------------------------------------------------------------------------------------------------
# create index for table: Position
whooshalchemy.whoosh_index(app, Position)
