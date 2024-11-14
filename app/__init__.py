from flask import Flask
from .routes import main as routes_blueprint  # Import the main blueprint from routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configurations from config.py

    # Register the blueprint
    app.register_blueprint(routes_blueprint)

    return app
