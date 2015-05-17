#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, CHAR, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

ENGINE = None
Session = None

Base = declarative_base()

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
    tags = relationship("Tag", secondary="feeds_tags", backref='rssfeeds') #this is an array


class Tag(Base):
    __tablename__ = "tags"
    uid = Column(String(32), primary_key = True, nullable=False)
    name = Column(String(64), nullable=False)
    display_phrase = Column(String(64), nullable=False)
    hierarchy = Column(String(32), nullable=False)
    codes = relationship("Ntee", foreign_keys='Ntee.tag_id', backref="issues")

class Ntee(Base):
    __tablename__ = "ntee"
    tag_id = Column(String(32), ForeignKey('tags.uid'))
    charity_id = Column(CHAR(10), ForeignKey('charities.eid'))
    code = Column(String(32), primary_key=True)
    name = Column(String(64))

class FeedTag(Base):
    __tablename__= "feeds_tags"
    rss_id = Column(CHAR(32), ForeignKey('rssfeeds.id'), primary_key=True)
    tag_id = Column(String(32), ForeignKey('tags.uid'), primary_key=True)

class Charity(Base):
   __tablename__ = 'charities'
   eid = Column(CHAR(10), primary_key=True)
   organization_name = Column(String(200), nullable=False, index=True)
   cover_photo = Column(String(200))    
   mission = Column(Text)
   city = Column(String(200), index=True)
   state = Column(String(100), index=True)
   zip_code = Column(String(10), index=True)
   logo_url = Column(String(200))
   aka_name = Column(String(200), index=True)
   geographic_areas_served = Column(Text)
   website_url = Column(String(200))
   year_founded = Column(Integer)
   codes = relationship("Ntee", foreign_keys='Ntee.charity_id', backref="charities")

def init_db(engine=None):
   if not engine:
       engine = get_engine()
       
   Base.metadata.drop_all(engine)
   Base.metadata.create_all(engine)
   return engine

def get_engine():
  # return create_engine('mysql://carebear:careBearCares4U@carebear.c0qcqj533aog.us-west-2.rds.amazonaws.com/carebear', echo=True) 
  # return create_engine('mysql://root@localhost/test99', echo=True)
    return create_engine('sqlite3:///rssfeed.db', echo=True)

def get_session(engine):    
  sess = scoped_session(sessionmaker(autoflush=True,
                                     autocommit=False))
  sess.configure(bind=engine)
  return sess

def main():
  # engine = init_db()
    db_session = get_session(get_engine)

if __name__ == "__main__":
    main()
