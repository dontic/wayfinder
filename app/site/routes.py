from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
import app.site.map_utils as map_utils
from plotly.utils import PlotlyJSONEncoder
import json
from app.auth.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from datetime import datetime, timedelta
from app.site.sql_cleanup import delete_duplicates

site = Blueprint('site', __name__)

@site.route('/')
@login_required
def overview():
    return render_template("site/overview.html", name=current_user.name)

@site.route('/pathmap', methods=['GET', 'POST'])
@login_required
def pathmap():
    date_i = (datetime.now() - timedelta(days=current_user.defaultPeriodPath)).strftime("%Y-%m-%dT%H:%M")
    date_f = datetime.now().strftime("%Y-%m-%dT%H:%M")
    date_min = datetime(2000,1,1,0,0,0).strftime("%Y-%m-%dT%H:%M")
    date_max = datetime.now().strftime("%Y-%m-%dT%H:%M")
    fig = map_utils.getPathPlot(current_user, date_i, date_f, showVisits=current_user.defaultShowVisits, removeIdle=current_user.defaultRemoveIdle, tripsColor=current_user.defaultTripColor)

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return render_template("site/pathmap.html", graphJSON=graphJSON, date_i=date_i, date_f=date_f, date_min=date_min, date_max=date_max)

@site.route('/visitsmap')
@login_required
def visitsmap():
    date_i = (datetime.now() - timedelta(days=current_user.defaultPeriodVisits)).strftime("%Y-%m-%dT%H:%M")
    date_f = datetime.now().strftime("%Y-%m-%dT%H:%M")
    date_min = datetime(2000,1,1,0,0,0).strftime("%Y-%m-%dT%H:%M")
    date_max = datetime.now().strftime("%Y-%m-%dT%H:%M")
    
    fig, missingHome = map_utils.getVisitsPlot(current_user, date_i, date_f, ignore_home=current_user.defaultIgnoreHome)
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template("site/visitsmap.html", graphJSON=graphJSON, date_i=date_i, date_f=date_f, date_min=date_min, date_max=date_max, missingHome=missingHome)

@site.route('/callback/<endpoint>')
@login_required
def cb(endpoint):
    if endpoint == 'visits_map':
        date_i = request.args.get('from_date')
        date_f = request.args.get('to_date')
        ignore_home = 'true' in request.args.get('ignore_home')
        fig, missingHome = map_utils.getVisitsPlot(current_user, date_i, date_f, ignore_home)
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        return graphJSON
    elif endpoint == 'path_map':
        date_i = request.args.get('from_date')
        date_f = request.args.get('to_date')
        showVisits = 'true' in request.args.get('show_visits')
        removeIdle = 'true' in request.args.get('remove_idle')
        tripsColor = 'true' in request.args.get('trips_color')
        fig = map_utils.getPathPlot(current_user, date_i, date_f, showVisits, removeIdle, tripsColor)
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        return graphJSON

@site.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        if request.form['button'] == 'mainsettings':
            # Changing plot settings
            defaultPeriodPath = request.form.get('defaultPeriodPath')
            maxAccuracyPath = request.form.get('maxAccuracyPath')
            defaultShowVisits = 'defaultShowVisits' in request.form
            defaultRemoveIdle = 'defaultRemoveIdle' in request.form
            defaultTripColor = 'defaultTripColor' in request.form
            defaultPeriodVisits = request.form.get('defaultPeriodVisits')
            defaultIgnoreHome = 'defaultIgnoreHome' in request.form
            user.defaultPeriodPath = defaultPeriodPath
            user.maxAccuracyPath = maxAccuracyPath
            user.defaultShowVisits = defaultShowVisits
            user.defaultRemoveIdle = defaultRemoveIdle
            user.defaultTripColor = defaultTripColor
            user.defaultPeriodVisits = defaultPeriodVisits
            user.defaultIgnoreHome = defaultIgnoreHome
            db.session.commit()
            message = 'Settings updated!'
            return render_template("site/settings.html", message=message, error=False, section='mainsettings', current_app=current_app)

        elif request.form['button'] == 'details':
            # Changing details
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')

            user_email = User.query.filter_by(email=email).first()
            if current_user.email != email and user_email:
                message = 'Email address already exists'
                return render_template("site/settings.html", message=message, error=True, section='details', current_app=current_app)
            
            user_username = User.query.filter_by(username=username).first()
            if current_user.username != username and user_username:
                message = 'Username already exists'
                return render_template("site/settings.html", message=message, error=True, section='details', current_app=current_app)
            
            user.name = name
            user.email = email
            user.username = username
            db.session.commit()
            message = 'Details updated!'
            return render_template("site/settings.html", message=message, error=False, section='details', current_app=current_app)

        elif request.form['button'] == 'password':
            password = request.form.get('password')
            new_password = request.form.get('newPassword')
            r_new_password = request.form.get('rNewPassword')

            if not check_password_hash(user.password, password):
                message = 'Wrong old password'
                return render_template("site/settings.html", message=message, error=True, section='password', current_app=current_app)

            if new_password != r_new_password:
                message = 'New passwords do not match'
                return render_template("site/settings.html", message=message, error=True, section='password', current_app=current_app)
            
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            message = 'Password changed!'
            return render_template("site/settings.html", message=message, error=False, section='password', current_app=current_app)

        elif request.form['button'] == 'api':
            apikey = request.form.get('apikey')
            user.apikey = generate_password_hash(apikey, method='sha256')
            db.session.commit()
            message = 'API key updated!'
            return render_template("site/settings.html", message=message, error=False, section='api', current_app=current_app)
        elif request.form['button'] == 'home':
            homeLAT = request.form.get('homeLAT')
            homeLONG = request.form.get('homeLONG')
            user.homeLAT = homeLAT
            user.homeLONG = homeLONG
            db.session.commit()
            message = 'Home coordinates updated!'
            return render_template("site/settings.html", message=message, error=False, section='home', current_app=current_app)
        elif request.form['button'] == 'cleanup':
            deldups, oldsize, newsize = delete_duplicates(current_user.username)
            message = 'Deleted %s duplicates and reduced the file size from %s MB to %s MB' % (deldups, oldsize, newsize)
            return render_template("site/settings.html", message=message, error=False, section='cleanup', current_app=current_app)

    return render_template("site/settings.html", current_app=current_app)

