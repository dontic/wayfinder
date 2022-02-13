from flask import Blueprint, render_template
from flask_login import login_required, current_user
import app.site.pathmap as path
import app.site.visitsmap as visits
from plotly.utils import PlotlyJSONEncoder
import json

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

@site.route('/visitsmap', methods=['GET', 'POST'])
@login_required
def visitsmap():
    date_i = None
    date_f = None
    fig = visits.getPlot(current_user, date_i, date_f)

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return render_template("site/visitsmap.html", graphJSON=graphJSON)