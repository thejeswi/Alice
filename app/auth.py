from . import app, login_manager
from .forms import LoginForm as LoginForm
from .models import *

from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

#~ try:
    #~ adminPassword = Config.query.all()[2].value
#~ except:
    #~ print "Adding Rollback login"
    #~ db.create_all()
    #~ settings = [["server-name","Alice"],["adminName","admin"],["password","password"]]
    #~ for setting in settings:
        #~ newConfig = Config(setting[0],setting[1])
        #~ db.session.add(newConfig)
    #~ db.session.commit()
    #~ adminPassword = settings[2][1]

ADMIN_AUTH={
        # username: password
        "expodad":"419dadexpo"
            }


class UserNotFoundError(Exception):
    pass


# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    '''Simple User class'''
    global ADMIN_AUTH
    USERS = ADMIN_AUTH
    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

