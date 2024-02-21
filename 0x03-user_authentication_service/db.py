#!/usr/bin/env python3
"""database moduel"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class for database"""

    def __init__(self) -> None:
        """ init values"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ memo session obj"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ returns user objec representing the nw one"""
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """ first row found in users table"""
        session = self.__session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a users attributes"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found". format(user_id))

        for k, v in kwargs.items():
            if not hasattr(user, k):
                raise ValueError("User has no attribute {}".format(k))
            setattr(user, k, v)

        try:
            self._session.commit()
        except IndentationError:
            raise ValueError("Invalid request")
