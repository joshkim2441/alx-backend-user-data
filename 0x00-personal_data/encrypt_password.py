#!/usr/bin/env python3
""" Password encryption and Validation"""
import bcrypt


def hash_password(password: str) -> bytes:
    """  Generates a salted and hashed password.

        Args:
                password (str): A string containing the plain text
                password to be hashed.

        Returns:
                bytes: A byte string representing the salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """  Validates whether the provided password matches the hashed password.

        Args:
                hashed_password (bytes): A byte string representing
                the salted, hashed password.
                password (str): A string containing the plain text
                password to be validated.

        Returns:
                bool: True if the provided password matches the hashed
                password, False otherwise.
    """
    valid = False
    if bcrypt.checkpw(password.encode(), hashed_password):
        valid = True
    return valid
