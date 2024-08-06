#!/usr/bin/env python3
""" Module of Basic Authentication
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ Extract Base64 string from header
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)$'
            match = re.fullmatch(pattern, authorization_header.strip())
        if match is not None:
            return match.group('token')
        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str
                                           ) -> str:
        """ Decode Base64-encoded authorization header
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(base64_authorization_header,
                                       validate=True)
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str
                                 ) -> Tuple[str, str]:
        """ Extract user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]*):(?P<passwd>.*)'
            match = re.fullmatch(pattern,
                                 decoded_base64_authorization_header.strip(),)
            if match is not None:
                return (match.group('user'), match.group('passwd'))
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                user = User.search({'email': user_email})
                if user is not None and len(user) > 0:
                    user = user[0]
                    if user.is_valid_password(user_pwd):
                        return user
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get current user from request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth = self.extract_base64_authorization_header(auth_header)
        if b64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(b64_auth)
        if decoded_auth is None:
            return None
        user_creds = self.extract_user_credentials(decoded_auth)
        if user_creds is None:
            return None
        user = self.user_object_from_credentials(user_creds[0], user_creds[1])
        if user is None:
            return None
        return user
