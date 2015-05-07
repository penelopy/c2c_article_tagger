from flask import Flask, render_template,request
import os
import sqlite3 as lite

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

class Article: 
    def __init__(self, summary_text, url, md5):
        self.summary_text = summary_text
        self.url = url
        self.md5 = md5
        self.tags = []

feed_data_list = []
list_of_article_objects = []
article_urls = []
md5_list = []
undo_list = []
list_of_tag_objects = []
tag_list = []


def read_data(): # refactor to only read-in the columns we want
    con = lite.connect('rssfeed.db')
    with con:    
        c = con.cursor()
        c.execute("SELECT * FROM Feeds")
        rows = c.fetchall()
        for row in rows: 
            feed_data_list.append(row)

read_data()






# def process_data():
for article in feed_data_list:
    url = article[1].encode('utf-8') 
    article_summary = article[3]  
    md5 = article[0]
    article_urls.append(url)
    article = Article(article_summary, url, md5)
    list_of_article_objects.append(article)
        # return list_of_article_objects, article_urls
# list_of_article_objects, article_urls = process_data()

article0 = list_of_article_objects[0]
# article01 = list_of_article_objects[1]

@app.route('/', methods=["GET", "POST"])
def home_page():
    # display_tag_list = display_tags_on_screen()
    tags_col1 = ["Advancing Science & Technology", "Autism", "Children's Diseases", "Curing Breast Cancer", "Curing Cancer", "Diseases", "HIV & Aids", "Improving Health Care"]
    tags_col2 = ["Improving Nutrition", "Mental Health", "Reproductive Rights", "Suicide Prevention", "Women's Health", "Supporting Services for Seniors", "Recreation & Fitness"]
    tags_col3 = ["Affordable Housing", "At-Risk Youth", "Civil Rights & Liberties", "Community Economic Development", "Domestic Violence Shelters & Services", "Feeding the Hungry", "Increasing Jobs", "Justice"]
    tags_col4 = ["LGBT Rights", "Women's Rights", "Trafficking and Exploitation", "Sports", "Supporting Arts & Culture", "None of the above", "Unclear", "Skip"]
    tags_col5 = ["Animal Welfare", "Disaster Relief", "Improving Education", "Protecting the Environment", "International Disaster Relief", "International Economic Development", "International Social Justice", "Services for Vets"]

    url = request.args.get('id2')
    url_prev = request.args.get('id1')
    tag = request.form.get('id')
    md5 = request.form.get('id7')
    jump = request.args.get('id4')
    undo = request.args.get('id5')

    if md5 is not None:
        md5_list.append(md5)

    if tag is not None:
        list_of_tag_objects.append(tag)

    if undo is not None:
        undo_tag(undo)

    if jump is not None:
        article1 = jump_to_untagged_article()
        return render_template("index.html", article=article1, first_tags=tags_col1, second_tags=tags_col2, third_tags=tags_col3, fourth_tags=tags_col4, fifth_tags=tags_col5)

    elif url is None and url_prev is None:
        return render_template("index.html", article=article0, first_tags=tags_col1, second_tags=tags_col2, third_tags=tags_col3, fourth_tags=tags_col4, fifth_tags=tags_col5)
    else:
        if url is not None:
            article1 = get_next_article(url, list_of_tag_objects, md5_list, undo_list)
            for i in range(len(list_of_tag_objects)):
                list_of_tag_objects.pop()
            return render_template("index.html", article=article1, first_tags=tags_col1, second_tags=tags_col2, third_tags=tags_col3, fourth_tags=tags_col4, fifth_tags=tags_col5)

        elif url_prev is not None:
            article1 = get_prev_article(url_prev)
            return render_template("index.html", article=article1, first_tags=tags_col1, second_tags=tags_col2, third_tags=tags_col3, fourth_tags=tags_col4, fifth_tags=tags_col5)

def display_tags_on_screen():
    tag_display_list = []
    tags_col1 = ["Advancing Science & Technology", "Autism", "Children's Diseases", "Curing Breast Cancer", "Curing Cancer", "Diseases", "HIV & Aids", "Improving Health Care"]
    tags_col2 = ["Improving Nutrition", "Mental Health", "Reproductive Rights", "Suicide Prevention", "Women's Health", "Supporting Services for Seniors", "Recreation & Fitness"]
    tags_col3 = ["Affordable Housing", "At-Risk Youth", "Civil Rights & Liberties", "Community Economic Development", "Domestic Violence Shelters & Services", "Feeding the Hungry", "Increasing Jobs", "Justice"]
    tags_col4 = ["LGBT Rights", "Women's Rights", "Trafficking and Exploitation", "Sports", "Supporting Arts & Culture", "None of the above", "Unclear", "Skip"]
    tags_col5 = ["Animal Welfare", "Disaster Relief", "Improving Education", "Protecting the Environment", "International Disaster Relief", "International Economic Development", "International Social Justice", "Services for Vets"]
    tag_display_list.append(tags_col1)
    tag_display_list.append(tags_col2)
    tag_display_list.append(tags_col3)    
    tag_display_list.append(tags_col4)
    tag_display_list.append(tags_col5)
    return tag_display_list

def jump_to_untagged_article():
    con = lite.connect('rssfeed.db')
    with con:    
        cur = con.cursor()
        cur.execute("SELECT * FROM tags WHERE ID = (SELECT MAX(ID) FROM tags)")
        items = cur.fetchone()
        for i in range(len(items)): 
            if i == 1: 
                md5 = items[i]
                cur.execute("SELECT * FROM feeds WHERE MD5=?", (md5,))

                feed_row = cur.fetchall()
                url = feed_row[0][1]

                index = article_urls.index(url)
                next_index = index + 1
                article = list_of_article_objects[next_index]
                return article

def get_next_article(url, tag_list, md5_list, undo_list):
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
            index = article_urls.index(url)
            next_index = index + 1
            article = list_of_article_objects[next_index]
            return article

def get_prev_article(url):
    if url is not None:
        index = article_urls.index(url)
        prev_index = index - 1
        article = list_of_article_objects[prev_index]
        return article

def undo_tag(undo): 
    if undo is not None:
        con = lite.connect('rssfeed.db')
        with con:    
            cur = con.cursor()
            cur.execute("DELETE FROM tags WHERE ID = (SELECT MAX(ID) FROM tags)")



if __name__ == "__main__":
    app.run(debug = True)