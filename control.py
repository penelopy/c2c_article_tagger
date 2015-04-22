from flask import Flask, render_template,request
import os
from model import con


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


article_data_list = []

with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Feeds")

    rows = cur.fetchall()
    for row in rows: 
        article_data_list.append(row)


list_of_article_objects = []

class Article: 
    def __init__(self, summary_text, url):
        self.summary_text = summary_text
        self.url = url
        self.tags = []


# class Tag: 
#     def __init__(self, tag_name):
#         self.tag_name = tag_name
#         self.url = url

article_summarys = []
article_urls = []
list_of_tag_objects = []


for article in article_data_list:
    if article[3] is not None:
        # summary = article[3].encode('utf-8')
        article_summarys.append(article[3])

    if article[0] is not None:
        url = article[1].encode('utf-8')
        article_urls.append(url)

for i in range(len(article_summarys)):
    article = Article(article_summarys[i], article_urls[i]) # query db and create instance of Article
    list_of_article_objects.append(article)

article0 = list_of_article_objects[0]


@app.route('/', methods=["GET", "POST"])
def home_page(): 
    possible_tags1 = ["Supporting Arts & Culture", "Improving Education", "Protecting the Environment", "Animal Welfare", "Improving Health Care", "Women's Health", "Mental Health"]
    possible_tags2 = ["Suicide Prevention", "Diseases", "Curing Cancer", "Curing Breast Cancer", "HIV & Aids", "Autism", "Children's Diseases"]
    possible_tags3 = ["Justice", "Trafficking and Exploitation", "Increasing Jobs", "Feeding the Hungry", "Improving Nutrition", "Affordable Housing", "Disaster Relief"]
    possible_tags4 = ["Recreation & Fitness", "At-Risk Youth", "Domestic Violence Shelters & Services", "Supporting Services for Seniors", "International Economic Development", "International Disaster Relief", "International Social Justice"]
    possible_tags5 = ["Civil Rights & Liberties", "Women's Rights", "LGBT Rights", "Reproductive Rights", "Community Economic Development", "Advancing Science & Technology", "Services for Vets"]    
    url = request.args.get('id2')
    url_prev = request.args.get('id1')
    tag = request.form.get('id')
    if tag is not None:
        list_of_tag_objects.append(tag)


    if url is None and url_prev is None:
        return render_template("index.html", article=article0, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)

    else:
        if url is not None:
            article1 = next_article(url)
            for i in range(len(list_of_tag_objects)):
                # item = list_of_tag_objects.pop()
                # PK = cur.execute("SELECT MD5 from feeds WHERE link = url")
                # cur.execute("INSERT INTO tags (MD5, link, tag_name) VALUES (PK, url, 'suicide')")
                # cur.commit()
                # article1.tags.append(item)
            # print "a= ", article1.tags
            # print "b= ", list_of_tag_objects
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)

        elif url_prev is not None:
            article1 = prev_article(url_prev)
            return render_template("index.html", article=article1, first_tags=possible_tags1, second_tags=possible_tags2, third_tags=possible_tags3, fourth_tags=possible_tags4, fifth_tags=possible_tags5, list_of_tag_objects=list_of_tag_objects)


def next_article(url):
    if url is not None:
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