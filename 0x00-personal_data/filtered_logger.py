#!/usr/bin/env python3
""" Returns filtered logs"""

import re
from typing import List

PII = {"name": "name", "email": "email", "phone": "phone",
       "ssn": "ssn", "password": "password"}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated by PII values"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator})', message)
    return message
