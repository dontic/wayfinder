from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.auth.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("auth/login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # Check user credentials
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('site.overview'))

@auth.route('/signup')
def signup():
    return render_template("auth/signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    apikey = request.form.get('apikey')

    user_email = User.query.filter_by(email=email).first()
    if user_email:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    user_username = User.query.filter_by(username=username).first()
    if user_username:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # Add new user to the sqlite database
    new_user = User(name=name, email=email, username=username, password=generate_password_hash(password, method='sha256'), apikey=generate_password_hash(apikey, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    # Sign in the user automatically
    user = User.query.filter_by(username=username).first()
    login_user(user, remember=False)

    return redirect(url_for('site.overview'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))