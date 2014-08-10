
__author__ = 'onyekaigabari'

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
