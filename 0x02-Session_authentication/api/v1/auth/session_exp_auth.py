#!/usr/bin/env python3
""" Module of expiration of Session Authentication
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Class of expiration of Session Authentication
    """
    def __init__(self):
        """ Initializes SessionExpAuth
        """
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            session_duration = int(SESSION_DURATION)
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        if self.seesion_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')

        if created_at is None:
            return None

        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return session_dict.get('user_id')
