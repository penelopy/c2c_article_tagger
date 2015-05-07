from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker, relationship

ENGINE = None
Session = None

Base = declarative_base()

feeds_tags = Table('feeds_tags', Base.metadata,
    Column('feed_tag_id', Integer, primary_key=True, nullable=False),
    Column('rss_id', Text, ForeignKey('rssfeeds.id'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tags.id'), nullable=False)
    )

class Feed():
    __tablename__ = "rssfeeds"
    id = Column(Text, primary_key=True, nullable=False)
    link = Column(Text)
    title = Column(Text)
    summary = Column(Text)
    source = Column(Text)
    published = Column(Text)
    timestamp = Column(Text)
    crawled = Column(Integer)

    tags = relationship("Tag", secondary=feeds_tags) #this is an array
    # type_of_center = relationship("Type", backref="centers")

class Tag():
    __tablename__ = "tags"
    id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String(32), nullable = False)

    feeds = relationship("Feed", secondary=feeds_tags) #this is an array



def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("mysql:///ph_test.db")
    Session = sessionmaker(bind=ENGINE)
    return Session()

db_session = connect()

def main():
    connect()
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()
