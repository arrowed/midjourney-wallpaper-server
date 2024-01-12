import os
import json
from dotenv import load_dotenv
from decorators.secured import secured

from flask import Flask, request, Response, jsonify, send_file
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
app.config.from_object(__name__)
app.debug = os.getenv("DEBUG", False)

app.config['allowed_keys'] = os.getenv("ALLOWED_KEYS","")
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.getenv("APP_KEY")


@app.route('/image', methods=["POST"])
@secured(app)
def add_image():
    if request.method == 'POST':
        print(request)
        print("/image")
        print(request.data)

        blob = json.loads(request.data)

        _add(blob['channel']['name'], blob)
        _add(blob['image']['classification'], blob)

    return Response(status=201)


@app.route('/image/<string:filename>', methods=["GET"])
@secured(app)
def get_image(filename):
    return send_file(os.path.join("..\\mj_wallpaperiser", filename))

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

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port="8080")
    socketio.run(app,host='0.0.0.0', port="8080", debug=True)
