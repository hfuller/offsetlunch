from flask import Flask
from web_ui.routes.tools import tools

from event_processor import EventProcessor

class WebUI:
    def __init__(self, db):
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = True

        self.app.config['db'] = db
        self.app.config['ep'] = EventProcessor(db)

        self.app.register_blueprint(tools)

    def go(self):
        self.app.run(host='0.0.0.0', port=5000)


