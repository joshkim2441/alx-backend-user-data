#!/usr/bin/env python3
""" Module of Auth
"""
import re
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if a path requires Authentication
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Get authorization header field from request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None
                     ) -> TypeVar('User'):  # type: ignore
        """ Get current user from request
        """
        return None

    def session_cookie(self, request=None):
        """ Get session cookie from request
        """
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None

        session_id = request.cookies.get(SESSION_NAME)

        return session_id
