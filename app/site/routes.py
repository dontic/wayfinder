from flask import Blueprint, render_template
from flask_login import login_required, current_user

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
@login_required
def overview():
    
    return render_template("site/overview.html")

@site.route('/mainmap', methods=['GET', 'POST'])
@login_required
def pathmap():
    
    return render_template("site/overview.html")

@site.route('/visitsmap', methods=['GET', 'POST'])
@login_required
def visitsmap():
    
    return render_template("site/overview.html")