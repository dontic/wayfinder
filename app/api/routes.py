from flask import Blueprint, request, jsonify
from app.api.data_processor import data_processor
from app.auth.models import User
from werkzeug.security import check_password_hash

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/overland/', methods=['GET', 'POST'])
def add_message(token=None):
    # Get json content
    print("Initializing API connection...")
    try:
        content = request.get_json()
        print("Got JSON content.")
    except:
        print("Received data not valid.")
        return(None)

    # Verify identity of the uploader
    print("Verifying user...")
    username = request.args.get("username")
    apikey = request.args.get("apikey")
    user = User.query.filter_by(username=username).first()
    # Check user credentials
    if not user or not check_password_hash(user.apikey, apikey):
        access = False
    else:
        access = True

    # Main script
    if access:
        data_processor(user, content)
        print("Returning confirmation to the client...")
        return jsonify({"result": "ok"})
        print("Done")
    else:
        return(None)