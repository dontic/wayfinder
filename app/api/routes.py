from flask import Blueprint, request, jsonify
import json
from app.api.data_processor import data_processor

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

    # Verify identity of the uploader
    print("Verifying user...")
    with open("users.json", "r") as f:
        auth = json.load(f)
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    
    if auth[user] == pwd:
        print("Identity verified.\nProcessing data for user: %s" % user)
        access = True
    else:
        access=False

    # Main script
    if access:
        data_processor(user, content)
        print("Returning confirmation to the client...")
        return jsonify({"result": "ok"})
        print("Done")
    else:
        return(None)