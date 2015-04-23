from flask import Flask, render_template,request
import os
import sqlite3 as lite

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

feed_data_list = []

def read_data():
    con = lite.connect('rssfeed.db')
    with con:    
        c = con.cursor()   
        c.execute("SELECT * FROM Feeds")
        rows = c.fetchall()
        for row in rows: 
            feed_data_list.append(row)

read_data()

list_of_article_objects = []

class Article: 
    def __init__(self, summary_text, url, md5):
        self.summary_text = summary_text
        self.url = url
        self.md5 = md5
        self.tags = []


# article_summarys = []
article_urls = []
# article_md5s = []
md5_list = []


for article in feed_data_list:
    url = article[1].encode('utf-8') 
    article_summary = article[3]  
    md5 = article[0]
    article_urls.append(url)
    article = Article(article_summary, url, md5)
    list_of_article_objects.append(article)

print "check this=", len(list_of_article_objects)
# for article in feed_data_list:
#     if article[3] is not None:
#         article_summarys.append(article[3])

#     if article[0] is not None:
#         article_md5s.append(article[0])

#     if article[1] is not None:
#         url = article[1].encode('utf-8')
#         article_urls.append(url)

# for i in range(len(article_summarys)):
#     article = Article(article_summarys[i], article_urls[i], article_md5s[i])
#     list_of_article_objects.append(article)

article0 = list_of_article_objects[0]
article01 = list_of_article_objects[1]
# print "hey hey", article01.url
# print article0.summary_text
# print article0.url
# print article.md5

# article0 = Article("Small, rarely seen vaquita verging on extinction; fishing limited to try to save it.", "http://www.utsandiego.com/news/2015/apr/16/endangered-vaquita-plan-save-gulf-california/", "a9b096d15f9a6110b8c08ad5d58904d4")
list_of_tag_objects = []
tag_list = []
@app.route('/', methods=["GET", "POST"])
def home_page():  
    possible_tags1 = ["Advancing Science & Technology", "Autism", "Children's Diseases", "Curing Breast Cancer", "Curing Cancer", "Diseases", "HIV & Aids", "Improving Health Care"]
    possible_tags2 = ["Improving Nutrition", "Mental Health", "Reproductive Rights", "Suicide Prevention", "Women's Health", "Supporting Services for Seniors", "Recreation & Fitness"]
    possible_tags3 = ["Affordable Housing", "At-Risk Youth", "Civil Rights & Liberties", "Community Economic Development", "Domestic Violence Shelters & Services", "Feeding the Hungry", "Increasing Jobs", "Justice"]
    possible_tags4 = ["LGBT Rights", "Women's Rights", "Trafficking and Exploitation", "Sports", "Supporting Arts & Culture", "None of the above", "Unclear", "Skip"]
    possible_tags5 = ["Animal Welfare", "Disaster Relief", "Improving Education", "Protecting the Environment", "International Disaster Relief", "International Economic Development", "International Social Justice", "Services for Vets"]

    url = request.args.get('id2')
    # print "id2 =", url
    url_prev = request.args.get('id1')
    tag = request.form.get('id')
    md5 = request.form.get('id7')
    # print "md5 =", md5
    skip = request.args.get('id4')
    print "skip =", skip

    if md5 is not None:
        md5_list.append(md5)

    if tag is not None:
        list_of_tag_objects.append(tag)

    if skip is not None:
        article1 = skip_to_untagged_article(skip)
        return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)

    elif url is None and url_prev is None:
        return render_template("index.html", article=article0, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)

    else:
        if url is not None:
            article1 = next_article(url, list_of_tag_objects, md5_list)
            for i in range(len(list_of_tag_objects)):
                list_of_tag_objects.pop()
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)

        elif url_prev is not None:
            article1 = prev_article(url_prev)
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)



def skip_to_untagged_article(skip):
    print "made it here", skip
    if skip is not None:
        # while True:
        con = lite.connect('rssfeed.db')
        with con:    
            cur = con.cursor()
            cur.execute("SELECT * FROM tags WHERE ID = (SELECT MAX(ID) FROM tags)")
            items = cur.fetchone()
            for i in range(len(items)): 
                if i == 1: 
                    print "last md5", items[i]
                    md5 = items[i]
                    # cur.execute("SELECT * FROM feeds WHERE MD5=?", md5)
                    # cur.execute("SELECT * FROM feeds WHERE MD5='cc85d32eb4159ba2fc326a7aac8e6093'")
                    cur.execute("SELECT * FROM feeds WHERE MD5=?", (md5,))

                    # select * from tags where MD5="cc85d32eb4159ba2fc326a7aac8e6093";


                    feed_row = cur.fetchall()
                    for item in feed_row: 
                        print "item=",item

                    for i in range(len(feed_row)):
                        if i == 1:
                            url = feed_row[i]
                            print "url", url
                            index = article_urls.index(url)
                            print "index", index
                            article = list_of_article_objects[index]
                            return article




            # for article in list_of_article_objects: 
            #     md5 = article.md5
            #     cur.execute("SELECT * FROM tags WHERE MD5=md5")
            #     items = cur.fetchone()
            #     for item in items: 
            #         if item is not None:
            #             print "zippy", item


def next_article(url, tag_list, md5_list):
    if url is not None:
        if md5_list != []:
            md5 = md5_list.pop()
            tags = ""
            for tag in tag_list:
                tags += tag + "," + " "
            con = lite.connect('rssfeed.db')
            with con:    
                cur = con.cursor()
                cur.execute("INSERT into tags (tag_name, MD5) VALUES (?, ?)", (tags, md5,))
            tags = ""
            tag_list = []
            # check_if_article_is_tagged()
            index = article_urls.index(url)
            next_index = index + 1
            article = list_of_article_objects[next_index]
            return article


"""

query feed table and check each record to see if that md5 also exists in the tag table - use while loop to keep checking until you find a md5 from feed that is NOT in tag. use this md5 to start diplaying the page. 
 """

def prev_article(url):
    if url is not None:
        index = article_urls.index(url)
        prev_index = index - 1
        article = list_of_article_objects[prev_index]
        return article

if __name__ == "__main__":
    app.run(debug = True)