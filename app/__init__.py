from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    
    # Register the routes blueprint
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
