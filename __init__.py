from flask import Flask
from view.main import main


def create_app():

    app = Flask(__name__, template_folder="_templates", static_folder="_static")
    app.register_blueprint(main)
    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=80)
