#!/usr/bin/env python3
""" module for session auth"""
import os
from typing import Tuple

from flask import abort, jsonify, request

from api.v1.app import auth
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> Tuple[str, int]:
    """ post login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(getattr(user[0], 'id'))
    rep = jsonify(user[0].to_json())
    rep.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return rep

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """ delete login session"""
    delete_session = auth.destroy_session(request)
    if not delete_session:
        abort(404)
    return jsonify({}), 200
