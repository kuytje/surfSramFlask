from flask import Flask

from auth_tools import get_code_challenge, get_config
from config import Config

def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    app.config.from_object(Config)

    # Extend the application config with DOTWELLKNOWN
    config_url = app.config['DOTWELLKNOWN']

    app.config.update(get_config(config_url))

    # Register blueprints
    with app.app_context():
        from application import routes
        app.register_blueprint(routes.app_blueprint)

    return app


# call the helper function to get the code verifier and code challenge
code_verifier, code_challenge = get_code_challenge()
