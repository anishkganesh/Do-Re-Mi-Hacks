import os
import secrets  # allows to create random hex name so that picture file names do not repeat
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required

# note: shift + tab to indent one tab space backwards
# note: alt + j to select next occurrence of highlighted text


@app.route("/")  # decorator
@app.route("/home")
def home():
    return render_template('index.html', title='Home')    # the variable posts can now be accessed from the html file


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # stores a string of random character (i.e. the hashed password) into hashed_password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data, specialization=None, location=None, musician_available=None, timings=None)
        db.session.add(user)
        db.session.commit()
        # second argument is a bootstrap class
        #flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('sign-up.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('sign-in.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/musician/searching")
def musician_searching():
    return render_template('musicianSearching.html',  title='Search')


@app.route("/company/searching")
def company_searching():
    return render_template('companySearching.html',  title='Search')


@app.route("/musician/profile")
def musician_profile():
    return render_template('musicianProfile.html',  title='Account')
