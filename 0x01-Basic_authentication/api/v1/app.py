#!/usr/bin/env python3
import os
from os import getenv
from typing import Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


auth_type = getenv("AUTH_TYPE", 'default')
if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth


@app.errorhandler(404)
def not_found(error) -> str:
    """ not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error: Exception) -> Tuple[jsonify, int]:
    """ unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 404


@app.errorhandler(403)
def forbidden(error: Exception) -> Tuple[jsonify, int]:
    """ forbidden handler"""
    return jsonify({"error": "forbidden"}), 404


@app.before_request
def handle_request():
    """ handle the requests by checking authentication and authorization
    of the user"""
    if auth is None:
        return

    # execluded paths
    execulded = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, execulded):
        return

    auth_hd = auth.authorization_header(request)
    if auth_hd is None:
        abort(401)
    user = auth.current_user(requests)
    if user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
