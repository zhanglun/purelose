#! usr/bin/env python3
from flask import Flask, make_response, jsonify
from app.models import mongo
from config import config

from app.views.home import home as home_blueprint
from app.views.api import api as api_blueprint


def create_app(config_name):
    app = Flask(__name__, template_folder="./templates")
    app.config.from_object(config[config_name])

    print(app.config)
    print(home_blueprint)

    config[config_name].init_app(app)
    mongo.init_app(app)

    app.register_blueprint(home_blueprint)
    app.register_blueprint(api_blueprint)

    @app.errorhandler(404)
    def http_error_handler(error):
        return make_response(jsonify({'error': 'Not found arer'}), 404)

    @app.errorhandler(500)
    def http_error_handler(error):
        return make_response(jsonify({'error': 'Server Error'}), 500)

    return app
