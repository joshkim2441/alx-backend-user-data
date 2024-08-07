#!/usr/bin/env python3
""" User Session module
"""
import uuid
from models.base import Base


class UserSession(Base):
    """ User Session class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Constructor
        """
        super().__init__(*args, **kwargs)
        if "user_id" not in kwargs:
            self.user_id = None
        if "session_id" not in kwargs:
            self.session_id = None
        if "expires" not in kwargs:
            self.expires = None
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.expires = kwargs.get('expires')
