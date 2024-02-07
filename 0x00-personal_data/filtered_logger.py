#!/usr/bin/env python3
"""A module for filtering the log"""
from typing import List
import re
# import os
# import logging
# import mysql.connector


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=([^{}]+)".format(field, separator)
        message = re.sub(pattern, "{}={}".format(field, redaction), message)
    return message
