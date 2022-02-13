from pickle import NONE
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import app.site.pathmap as path
import app.site.visitsmap as visits
from plotly.utils import PlotlyJSONEncoder
import json
from app.auth.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

site = Blueprint('site', __name__)

@site.route('/')
@login_required
def overview():
    return render_template("site/overview.html", name=current_user.name)

@site.route('/mainmap', methods=['GET', 'POST'])
@login_required
def pathmap():
    date_i = None
    date_f = None
    fig = path.getPlot(current_user, date_i, date_f)

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return render_template("site/pathmap.html", graphJSON=graphJSON)

@site.route('/visitsmap')
@login_required
def visitsmap():
    date_i = None
    date_f = None
    ignore_home = None
    
    fig = visits.getPlot(current_user, date_i, date_f, ignore_home)
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template("site/visitsmap.html", graphJSON=graphJSON, ignore_home_value=None)

@site.route('/callback/<endpoint>')
@login_required
def cb(endpoint):
    if endpoint == 'visits_map':
        ignore_home = request.args.get('ignore_home')
        date_i = request.args.get('from_date')
        date_f = request.args.get('to_date')
        print(ignore_home, date_i, date_f)
        fig = visits.getPlot(current_user, date_i, date_f, ignore_home)
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        return graphJSON
    else:
        print('ERROR')

@site.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        if request.form['button'] == 'details':
            # Changing details
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')

            user_email = User.query.filter_by(email=email).first()
            if current_user.email != email and user_email:
                message = 'Email address already exists'
                return render_template("site/settings.html", message=message, error=True, section='details')
            
            user_username = User.query.filter_by(username=username).first()
            if current_user.username != username and user_username:
                message = 'Username already exists'
                return render_template("site/settings.html", message=message, error=True, section='details')
            
            user.name = name
            user.email = email
            user.username = username
            db.session.commit()
            message = 'Details updated!'
            return render_template("site/settings.html", message=message, error=False, section='details')

        elif request.form['button'] == 'password':
            password = request.form.get('password')
            new_password = request.form.get('newPassword')
            r_new_password = request.form.get('rNewPassword')

            if not check_password_hash(user.password, password):
                message = 'Wrong old password'
                return render_template("site/settings.html", message=message, error=True, section='password')

            if new_password != r_new_password:
                message = 'New passwords do not match'
                return render_template("site/settings.html", message=message, error=True, section='password')
            
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            message = 'Password changed!'
            return render_template("site/settings.html", message=message, error=False, section='password')

        elif request.form['button'] == 'api':
            apikey = request.form.get('apikey')
            user.apikey = generate_password_hash(apikey, method='sha256')
            db.session.commit()
            message = 'API key updated!'
            return render_template("site/settings.html", message=message, error=False, section='api')
        elif request.form['button'] == 'home':
            homeLAT = request.form.get('homeLAT')
            homeLONG = request.form.get('homeLONG')
            user.homeLAT = homeLAT
            user.homeLONG = homeLONG
            db.session.commit()
            message = 'API key updated!'
            return render_template("site/settings.html", message=message, error=False, section='home')

    return render_template("site/settings.html")

