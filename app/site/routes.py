from flask import Blueprint, render_template

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def overview():
    
    return render_template("site/overview.html")

@site.route('/mainmap', methods=['GET', 'POST'])
def pathmap():
    
    return render_template("site/overview.html")

@site.route('/visitsmap', methods=['GET', 'POST'])
def visitsmap():
    
    return render_template("site/overview.html")