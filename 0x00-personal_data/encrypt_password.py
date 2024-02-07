#!/usr/bin/env python3
"""module that encrypt the passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed password of a user"""
    slt = bcrypt.genselt()
    return bcrypt.haspw(password.encode("utf-8"), slt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that expects 2 arguments and returns a boolean."""
    return bcrypt.checkpw(password.encode("utf-8"), hash_password)
