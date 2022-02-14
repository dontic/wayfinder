from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.auth.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app.auth.signup import process_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
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

    return render_template("auth/login.html")


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        return process_user(request)

    return render_template("auth/signup.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))