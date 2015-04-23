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


article_summarys = []
article_urls = []
article_md5s = []
list_of_tag_objects = []
md5_list = []


for article in feed_data_list:
    if article[3] is not None:
        article_summarys.append(article[3])

    if article[0] is not None:
        article_md5s.append(article[0])

    if article[1] is not None:
        url = article[1].encode('utf-8')
        article_urls.append(url)

for i in range(len(article_summarys)):
    article = Article(article_summarys[i], article_urls[i], article_md5s[i])
    list_of_article_objects.append(article)

article0 = list_of_article_objects[0]


@app.route('/', methods=["GET", "POST"])
def home_page():  
    possible_tags1 = ["Advancing Science & Technology", "Autism", "Children's Diseases", "Curing Breast Cancer", "Curing Cancer", "Diseases", "HIV & Aids", "Improving Health Care"]
    possible_tags2 = ["Improving Nutrition", "Mental Health", "Reproductive Rights", "Suicide Prevention", "Women's Health", "Supporting Services for Seniors", "Recreation & Fitness" ]
    possible_tags3 = ["Affordable Housing", "At-Risk Youth", "Civil Rights & Liberties", "Community Economic Development", "Domestic Violence Shelters & Services", "Feeding the Hungry", "Increasing Jobs", "Justice"]
    possible_tags4 = ["LGBT Rights", "Women's Rights", "Trafficking and Exploitation", "Sports", "Supporting Arts & Culture", "None of the above", "Unclear", "Skip"]
    possible_tags5 = ["Animal Welfare", "Disaster Relief", "Improving Education", "Protecting the Environment", "International Disaster Relief", "International Economic Development", "International Social Justice", "Services for Vets"]

    url = request.args.get('id2')
    url_prev = request.args.get('id1')

    tag = request.form.get('id')

    md5 = request.form.get('id7')

    if md5 is not None:
        md5_list.append(md5)

    if tag is not None:
        list_of_tag_objects.append(tag)

    if url is None and url_prev is None:
        return render_template("index.html", article=article0, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)

    else:
        if url is not None:
            article1 = next_article(url, list_of_tag_objects, md5_list)
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)

        elif url_prev is not None:
            article1 = prev_article(url_prev)
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)


def next_article(url, list_of_tag_objects, md5_list):
    tags = ""
    if url is not None:
        print "md5 list =", md5_list
        if md5_list != []:
            md5 = md5_list.pop()
            for tag in list_of_tag_objects:
                tags += tag + "," + " "
            print "tags=", tags
            con = lite.connect('rssfeed.db')
            with con:    
                cur = con.cursor()
                cur.execute("INSERT into tags (tag_name, MD5) VALUES (?, ?)", (tags, md5,))
                tags = ""

        index = article_urls.index(url)
        next_index = index + 1
        article = list_of_article_objects[next_index]
        return article

def prev_article(url):
    if url is not None:
        index = article_urls.index(url)
        prev_index = index - 1
        article = list_of_article_objects[prev_index]
        return article

if __name__ == "__main__":
    app.run(debug = True)