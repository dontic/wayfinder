from flask import Flask, request, jsonify
from data_processor import data_processor
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    # Main flask map interface
    # In developement
    pass

@app.route('/api/', methods=['GET', 'POST'])
def add_message(token=None):
    # Gather json content
    try:
        content = request.get_json()
    except:
        print("Format data not valid.")

    # Verify identity of the uploader
    with open("users.json", "r") as f:
        auth = json.load(f)
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    
    if auth[user] == pwd:
        print("Identity verified.\nGetting data from user: %s" % user)
        access = True
    else:
        access=False

    # Main script
    if access:
        data_processor(user, content)
        return jsonify({"result": "ok"})
    else:
        return(None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)