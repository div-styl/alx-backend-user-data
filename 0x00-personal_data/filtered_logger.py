#!/usr/bin/env python3
"""A module for filtering the log"""
from typing import List
import re
import os
import logging
import mysql.connector
# from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=([^{}]+)".format(field, separator)
        message = re.sub(pattern, "{}={}".format(field, redaction), message)
    return message


def get_logger() -> logging.Logger:
    """ return the logging logger obj"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handle = logging.StreamHandler()
    handle.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handle)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connector to a database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=db_name
    )

    return connection


def main() -> None:
    """Display the rows of db"""
    db = get_db()
    csr = db.cursor()
    csr.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in csr:
        msg = (
            "name={};email={};phone={};ssn={};password={};ip={};"
            "last_login={};user_agent={};".format(*row)
        )
        logger.info(msg)
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """fomrt the fitered"""
        notsafe_str = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, notsafe_str, self.SEPARATOR
        )
