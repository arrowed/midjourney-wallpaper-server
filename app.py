import os
import json
from dotenv import load_dotenv
from decorators.secured import secured

from flask import Flask, request, Response, jsonify, send_from_directory, redirect
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
app.config.from_object(__name__)
app.debug = os.getenv("DEBUG", False)

app.config['allowed_keys'] = os.getenv("ALLOWED_KEYS","")
app.config['image_base_folder'] = os.getenv("IMAGE_ROOT_FOLDER","../,images")
app.config['webapp_base_folder'] = os.getenv("WEBAPP_ROOT_FOLDER","../,app")

app.config['JSON_AS_ASCII'] = False
app.secret_key = os.getenv("APP_KEY")


@app.route('/image', methods=["POST"])
@secured(app)
def add_image():
    if request.method == 'POST':
        blob = json.loads(request.data)

        _add(blob['channel']['name'], blob)
        _add(blob['image']['classification'], blob)

    return Response(status=201)

@app.route('/image/<path:filename>', methods=["GET"])
def get_image(filename):
    return send_from_directory(app.config['image_base_folder'], filename)

@app.route('/topics', methods=["GET"])
def get_topics():
    topics = [t.decode('UTF-8') for t in app.config['red'].keys("image-*")]
    print(topics)
    return jsonify({"topics": topics})

def _add(key, json_blob):
    socketio.emit(key, json_blob)

# Event for handling new connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')


# Event for handling disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# Static resources hosting
@app.route('/', methods=["GET"])
def get_homepage():
    return redirect("/index.html")

@app.route('/asset-manifest.json', methods=["GET"])
def get_app_asset_manifest():
    return _get_static_resource("asset-manifest.json")
@app.route('/favicon.ico', methods=["GET"])
def get_app_favicon():
    return _get_static_resource("favicon.ico")
@app.route('/index.html', methods=["GET"])
def get_app_index():
    return _get_static_resource("index.html")
@app.route('/logo192.png', methods=["GET"])
def get_app_logo192():
    return _get_static_resource("logo192.png")
@app.route('/logo512.png', methods=["GET"])
def get_app_logo512():
    return _get_static_resource("logo512.png")
@app.route('/manifest.json', methods=["GET"])
def get_app_manifest():
    return _get_static_resource("manifest.json")
@app.route('/robots.txt', methods=["GET"])
def get_app_robots():
    return _get_static_resource("robots.txt")

@app.route('/static/<path:name>', methods=["GET"])
def get_static_resource(name):
    return send_from_directory(os.path.join(app.config['webapp_base_folder'], "static"), name)
@app.route('/static/js/<path:name>', methods=["GET"])
def get_static_js_resource(name):
    return send_from_directory(os.path.join(app.config['webapp_base_folder'], "static", "js"), name)
@app.route('/static/css/<path:name>', methods=["GET"])
def get_static_css_resource(name):
    return send_from_directory(os.path.join(app.config['webapp_base_folder'], "static", "css"), name)

def _get_static_resource(filename):
    location = os.path.join(app.config['webapp_base_folder'], filename)
    print(location)
    return send_from_directory(app.config['webapp_base_folder'], filename)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port="8080")
    socketio.run(app,host='0.0.0.0', port="8080", debug=True)
