import csv
# from model import con
import sqlite3 as lite

# with con:    
#     cur = con.cursor() 

# def load_tags(cur):
#     f = open('seed_data/tags.csv','r')
#     f = f.read().split("\r")

#     for line in f:
#         fields = line.split(',')
#         tag_name = fields[1]
#         cur.execute("INSERT INTO Tags(name) VALUES (tag_name)")
#         # cur.commit()



# def main(cur):
#     load_tags(cur)
#     cur.commit()
#     cur.close()

# if __name__ == "__main__":
#     # session = model.connect()
#     # session = model.db_session
#     main(cur)

# with open('feeds.csv', 'w') as csvfile:
#     fieldnames = ['md5', 'title', 'summary', 'source', 'published', 'timestamp', 'crawled', 'tags']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # writer.writeheader()
    # writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

export_data_list = []
def export_to_tsv():
    # file = open('test.csv', 'w');
    # writer = csv.writer(file)
    # with open('feeds.csv', 'w') as csvfile:
    #     fieldnames = ['md5', 'title', 'summary', 'source', 'published', 'timestamp', 'crawled', 'tags']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    con = lite.connect('rssfeed.db')
    with con:    
        c = con.cursor()
        c.execute("SELECT * FROM feeds LEFT OUTER JOIN tags ON feeds.MD5=tags.MD5")
        rows = c.fetchall()
        for row in rows: 
            url = row[1].encode('utf-8') 
            md5 = row[4]
            print md5

            # writer.writeheader()
            # writer.writerow({'md5': row[0], 'title': row[2], 'summary': row[3], 'source': url, 'published': })

            # export_data_list.append(row)
    #         writer.writerow(row)
    # file.close()
export_to_tsv()




    # new_feed = model.Feed(id = id, 
    #                       link = link, 
    #                       title = title, 
    #                       summary = summary, 
    #                       source = source, 
    #                       published = published, 
    #                       timestamp = timestamp, 
    #                       crawled = crawled, 
    #                             )