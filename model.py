import sqlite3 as lite
# import sys
# import codecs

article_data_list = []
con = lite.connect('test.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Feeds")

    rows = cur.fetchall()
    for row in rows: 
        article_data_list.append(row)
# return article_data_list



# def save_output_to_txt_file(rows, output_filename):
#     with codecs.open(output_filename, 'w', encoding="utf-8") as f:
#         for row in rows: 
#             f.write('%s' % ('\t'.join(row) + '\n'))

# save_output_to_txt_file(rows, 'complete_article_list.txt')    

    # for row in rows:
    #     print "******************"
    #     print "ARTICLE DATA"

    #     # for item in row: 
    #     #     print item


    #     link = row[0]
    #     title = row[1]
    #     summary = row[2]
    #     rss_source_url = row[3]
    #     published = row[4]
    #     timestamp = row[5]

        # print link
        # print title

#     link = Column(String(32), primary_key = True, nullable = False)
#     title = Column(String(32), nullable = False)
#     summary = Column(String(32), nullable = False)
#     rss_source_url = Column(String(32), nullable = False)
#     published = Column(String(32), nullable = False)
#     timestamp = Column(String(32), nullable = False)


# cur.execute("INSERT INTO Friends(Name) VALUES ('Tom');")

#  cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT);")


class Article():
    __tablename__ = "articles"
    id = Column(String(32), primary_key = True, nullable=False)
    title = Column(String(32), nullable = False)
    summary = Column(String(32), nullable = False)
    rss_source_url = Column(String(32), nullable = False)
    published = Column(String(32), nullable = False)
    timestamp = Column(String(32), nullable = False)

class Tag():
    __tablename__ = "tags"
    id = Column(Integer(6), primary_key = True, nullable=False)
    tag_name = Column(String(32), nullable = False)

articles_tags = Table('articles_tags', Base.metadata, 
    Column('article_tag_id', Integer, primary_key=True, nullable=False), 
    Column('link', String, ForeignKey('articles.link'), nullable=False),
    Column('tags_id', Integer, ForeignKey('tags.id'), nullable=False)
    )


def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///test.db", echo=True)
    Session = sessionmaker(bind=ENGINE)
    return Session()

db_session = connect()

def main():
    connect()
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()

