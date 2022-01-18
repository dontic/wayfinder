from flask import Flask, request, jsonify
from data_processor import handle_data
import json

app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
def add_message(token=None):
    # Gather json content
    try:
        content = request.get_json()
    except:
        print("Format data not valid.")

    # Get authorisation
    with open("users.json", "r") as f:
        auth = json.load(f)
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    
    if auth[user] == pwd:
        print("Identity verified.\nGetting data from user: %s" % user)
        access = True
    else:
        access=False

    # Verify identity of the uploader
    if access:
        handle_data(user, content)
        return jsonify({"result": "ok"})
    else:
        return(None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)