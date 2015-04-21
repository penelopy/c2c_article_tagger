from flask import Flask, render_template,request
# from flask import session as flask_session
import os
# import model
# import csv


import sqlite3 as lite
import sys
import codecs

article_data_list = []
con = lite.connect('test.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Feeds")

    rows = cur.fetchall()
    for row in rows: 
        article_data_list.append(row)


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


list_of_article_objects = []

class Article: 
    def __init__(self, summary_text, url):
        self.summary_text = summary_text
        self.url = url
        self.tags = []

article_summarys = []
article_urls = []


for article in article_data_list:
    if article[3] is not None:
        # summary = article[3].encode('utf-8')
        article_summarys.append(article[3])

    if article[0] is not None:
        url = article[0].encode('utf-8')
        article_urls.append(url)

for i in range(len(article_summarys)):
    article = Article(article_summarys[i], article_urls[i]) # query db and create instance of Article
    list_of_article_objects.append(article)

article0 = list_of_article_objects[0]


@app.route('/', methods=["GET", "POST"])
def home_page(): 
    possible_tags1 = ["Supporting Arts & Culture", "Improving Education", "Protecting the Environment", "Animal Welfare", "Improving Health Care", "Women's Health", "Mental Health"]
    possible_tags2 =["Suicide Prevention", "Diseases", "Curing Cancer", "Curing Breast Cancer", "HIV & Aids", "Autism", "Children's Diseases"]
    possible_tags3 = ["Justice", "Trafficking and Exploitation", "Increasing Jobs", "Feeding the Hungry", "Improving Nutrition", "Affordable Housing", "Disaster Relief"]
    possible_tags4 = ["Recreation & Fitness", "At-Risk Youth", "Domestic Violence Shelters & Services", "Supporting Services for Seniors", "International Economic Development", "International Disaster Relief", "International Social Justice"]
    possible_tags5 = ["Civil Rights & Liberties", "Women's Rights", "LGBT Rights", "Reproductive Rights", "Community Economic Development", "Advancing Science & Technology", "Services for Vets"]    
    # url_prev = request.args.get('id1')
    url = request.args.get('id2')
    url_prev = request.args.get('id1')

    if url is None and url_prev is None:
        return render_template("index.html", article=article0, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)
    else:
        if url is not None:
            # index = article_urls.index(url)
            # if index > last_index: 
            print "next= ", url
            article1 = next_article(url)
            # print "new article url", article1.url
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)
        elif url_prev is not None:
            print "prev= ", url_prev
            article1 = prev_article(url_prev)
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5)


def next_article(url):
    if url is not None:
        index = article_urls.index(url)
        next_index = index + 1
        article = list_of_article_objects[next_index]
        # print "next url", article.url
        return article

def prev_article(url):
    if url is not None:
        index = article_urls.index(url)
        prev_index = index - 1
        article = list_of_article_objects[prev_index]
        # print "next url", article.url
        return article


    # if id is not None:
    #     article.tags.append(id)



if __name__ == "__main__":
    app.run(debug = True)