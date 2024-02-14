#!/usr/bin/env python3
"""Module session db auth
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ session db auth """
    pass