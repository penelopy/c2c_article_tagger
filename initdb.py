#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, CHAR, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

Base = declarative_base()

feeds_tags = Table('feeds_tags', Base.metadata,
    Column('rss_id', CHAR(32), ForeignKey('rssfeeds.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')))

class Feed(Base):
    __tablename__ = "rssfeeds"
    id = Column(CHAR(32), primary_key=True, nullable=False)
    link = Column(Text)
    title = Column(Text)
    summary = Column(Text)
    source = Column(Text)
    published = Column(Text)
    timestamp = Column(Text)
    crawled = Column(Integer)
    tags = relationship("Tag", secondary=feeds_tags, backref='rssfeeds') #this is an array


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String(32), nullable = False)

def get_engine():
   return create_engine('mysql://)    

def get_session(engine):    
   sess = scoped_session(sessionmaker(autoflush=True,
                                      autocommit=False))
   sess.configure(bind=engine)
   return sess
           
def init_db(engine=None):
   if not engine:
       engine = get_engine()
       
   Base.metadata.drop_all(engine)
   Base.metadata.create_all(engine)


def main():
    init_db()
    # db = get_session(engine)

if __name__ == "__main__":
    main()
