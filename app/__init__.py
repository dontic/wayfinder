# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.api.routes import api
from app.site.routes import site

# Register blueprint(s)
app.register_blueprint(api)
app.register_blueprint(site)
# app.register_blueprint(xyz_module)
# ..