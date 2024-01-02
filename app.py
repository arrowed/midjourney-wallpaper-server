import redis

import os
import json
from dotenv import load_dotenv
from decorators.secured import secured

from flask import Flask, request, Response, jsonify


load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = os.getenv("DEBUG", False)

if (os.getenv("REDIS_USER", "") == ""):
    app.config['red'] = redis.StrictRedis(host=os.getenv("REDIS_SERVER", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)))
else:
    app.config['red'] = redis.StrictRedis(host=os.getenv("REDIS_SERVER", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), username=os.getenv("REDIS_USER"), password=os.getenv("REDIS_USER"))

app.config['allowed_keys'] = os.getenv("ALLOWED_KEYS","")
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.getenv("APP_KEY")

app.config['red'].set('token', app.config['allowed_keys'])

@app.route('/')
@secured(app)
#@cached(app)
def index():
    folders= [u.decode('utf-8')[7:] for u in app.config['red'].keys('folder:*')]
    
    return render_template('main.html', next=url_for('index'), recent_folders=folders)

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

@app.route('/topics', methods=["GET"])
# @secured(app)
def get_topics():
    topics = [t.decode('UTF-8') for t in app.config['red'].keys("image-*")]
    print(topics)
    return jsonify({"topics": topics})


def _add(key, json_blob):
    app.config['red'].lpush(f"image-{key}", json.dumps(json_blob))
    app.config['red'].publish(f"image-{key}", json.dumps(json_blob))

    app.config['red'].ltrim(key, 0, 1000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8080")
