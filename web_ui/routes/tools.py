from flask import current_app, Blueprint, jsonify

tools = Blueprint('tools', __name__, url_prefix='/tools')

@tools.record
def record(state):
    if state.app.config.get("ep") is None:
        raise Exception("Please provide the event processor object in the ep state var")

@tools.route("/poll")
def poll():
    current_app.config["ep"].poll_sources()
    return jsonify(True)

