from flask import Flask
from view.main import main


def create_app():

    app = Flask(__name__, template_folder="_templates", static_folder="_static")
    app.register_blueprint(main)
    return app
