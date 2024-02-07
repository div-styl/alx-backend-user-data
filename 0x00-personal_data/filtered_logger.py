#!/usr/bin/env python3
"""A module for filtering"""
import os
import re
import logging
# import mysql.connector
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str):
    """returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=([^{}]+)".format(field, separator)
        message = re.sub(pattern, "{}={}".format(field, redaction), message)
    return message
