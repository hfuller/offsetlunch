from flask import Flask
from routes.tools import tools

class WebUI:
    def __init__(self, ep):
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = True
        self.app.config['ep'] = ep
        self.app.register_blueprint(tools)

    def go(self):
        self.app.run(host='0.0.0.0', port=5000)


