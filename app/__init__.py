from flask import Flask, render_template
from config import Config
from flask_login import LoginManager
from app.extensions import db
from flask_login import LoginManager

def create_app():
    # Define the WSGI application object
    app = Flask(__name__, static_url_path="", static_folder="static")

    # Configurations
    app.config.from_object(Config)

    # Authentication stuff
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.auth.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Import modules using their blueprint handler variable
    from app.api.routes import api
    from app.site.routes import site
    from app.auth.routes import auth

    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(auth)

    return app