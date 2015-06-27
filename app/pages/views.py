from server import app
from server import admin_required

from .models import *
from .run  import *

from flask import Flask, request, flash, url_for, redirect, render_template, abort, g,session
from flask.ext.login import login_required, login_user
               
@simple_page.route('/')
def index():
    return "hello"

@simple_page.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user_login = User.query.filter_by(email=email).first()
        g.user = user_login
        if user_login is None:
            flash('Email is invalid','error')
            return redirect(url_for('simple_page.login'))
        if not user_login.check_password(password):
            flash('Password is invalid','error')
            return redirect(url_for('simple_page.login'))
        login_user(user_login, remember = False)
        flash(request.form['username']+' has logged in.')
        return redirect(url_for('simple_page.index'))
    else:
        return render_template('login.html', error=error)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@simple_page.route('/add', methods=['GET', 'POST'])
@admin_required
def addUser():
	if request.method ==  'GET':
		return render_template('adduser.html')
	else:
		user = User(request.form['name'],request.form['password'],request.form['email'],0)
		db.session.add(user)
		db.session.commit()
		flash(u'User for '+request.form['name']+' was successfully created')
		return redirect(url_for('simple_page.users'))

@simple_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('simple_page.index')) 


@simple_page.route('/remove/<int:user_id>')
@admin_required
def removeUser(user_id):
	user = User.query.filter_by(id = user_id).first()
	flash("Removed User "+ user.name)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('simple_page.users'))


@simple_page.route('/users')
@admin_required
def users():
	users = User.query.all()
	return render_template('listusers.html', users = users, student = False)



@simple_page.route('/change_password', methods = ['GET' , 'POST'])
@login_required
def change_password():
	user = g.user.id
	user = User.query.filter_by(id = user).first()
	if request.method == 'GET':
		return render_template('change_password.html', loggedIn = True)
	if user.check_password(request.form['current_password']):
		user.set_password(request.form['new_password'])
		db.session.commit()
		flash("Password has been updated")
	else:
		flash("Wrong password")
		return redirect(url_for('simple_page.login'))
	return redirect(url_for('simple_page.index'))

