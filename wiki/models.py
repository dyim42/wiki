#coding=utf8
from . import app
from sqlalchemy import Column, Integer, Text, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

# application database backend
here = os.path.abspath(os.path.dirname(__file__))
db_url = app.config['DB_URL'] % dict(here=here)
db_engine = create_engine(db_url, convert_unicode=True, echo=app.debug)
db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()

@app.teardown_request
def shutdown_session(exception=None):
    global db_session
    db_session.remove()

def init_db():
    """Create the underlying database schema"""
    Base.metadata.create_all(bind=db_engine)


class Page(Base):
    """Page object, heart of the wiki"""

    __tablename__ = 'page'

    name = Column(String(256), primary_key=True, index=True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data
