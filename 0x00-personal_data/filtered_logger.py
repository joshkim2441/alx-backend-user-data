#!/usr/bin/env python3
""" Returns filtered logs"""

import re
import logging
import mysql.connector
from os import environ
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = {"name", "email", "phone", "ssn", "password"}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated by PII values"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """ Returns a logger object"""
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector object to a MySQL database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME", "")
    cnnect = mysql.connector.connection.MySQLConnection(
        user=username,
        port=3306,
        password=password,
        host=host,
        database=db_name
        )
    return cnnect


def main() -> None:
    """ Obtain a database connection using get_db and retrieves all rows
    in the users table and display each row under a filtered format
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cols = fields.split(",")
    db = get_db()
    cur = db.cursor()
    query = ("SELECT * FROM users;")
    logger = get_logger()
    with cur() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in cursor:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(cols, row),
            )

        str_row = '{};'.format('; '.join(list(record)))
        args = ("user_data", logging.INFO, None, None, str_row, None, None)
        log_rec = logging.LogRecord(*args)
        logger.handle(log_rec)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        msg = super(RedactingFormatter, self).format(record)
        rec = filter_datum(self.fields, self.REDACTION,
                           msg, self.SEPARATOR)
        return rec


if __name__ == "__main__":
    main()
