from flask import Flask, jsonify, send_from_directory
import os

from sensors import get_sensors
from system_stats import get_system
from tasks import get_tasks

app = Flask(__name__, static_folder=None)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/sensors")
def api_sensors():
    return jsonify(get_sensors())


@app.route("/api/system")
def api_system():
    return jsonify(get_system())


@app.route("/api/tasks")
def api_tasks():
    return jsonify(get_tasks())


@app.route("/api/all")
def api_all():
    return jsonify({
        "sensors": get_sensors(),
        "system": get_system(),
        "tasks": get_tasks(),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
