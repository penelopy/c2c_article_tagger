from flask import Flask, render_template, redirect, url_for, request
from flask import session as flask_session
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


list_of_article_objects = []

class Article: 
    def __init__(self, summary_text, url):
        self.summary_text = summary_text
        self.url = url
        self.tags = []

summary_text = [
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc finibus et mauris a commodo. Cras vitae metus scelerisque, feugiat nisl et, mattis dui. Proin est est, viverra ac rhoncus a, interdum nec lacus. Cras eget vulputate massa, elementum aliquet felis. Nunc felis libero, eleifend eget arcu nec, bibendum interdum nulla. Curabitur molestie felis ante, condimentum fringilla velit convallis ut. Aenean sit amet arcu porttitor, molestie risus nec, sollicitudin leo. Donec consequat maximus viverra. Donec magna arcu, vulputate vitae imperdiet tincidunt, tincidunt eget arcu. In in odio scelerisque, lacinia sem eget, imperdiet enim. Quisque erat odio, cursus vitae efficitur id, blandit in augue. Cras eu tellus leo. Sed eu quam in mauris pharetra condimentum. Fusce vehicula dictum maximus. Cras rutrum nec mi id tempus.",
"Integer nec velit tortor. Aliquam suscipit viverra arcu sed pretium. Mauris eu commodo nisi, a lacinia nulla. Maecenas at felis et dolor tincidunt rhoncus non eget purus. Morbi ut urna ullamcorper, rutrum urna vel, porttitor est. Etiam massa ipsum, maximus at justo ac, tristique tempor odio. Mauris laoreet et urna quis tincidunt. Proin ornare, tellus in rutrum varius, sapien neque semper quam, a lacinia magna purus ac sem.",
"Quisque neque massa, feugiat at iaculis at, feugiat non ligula. Curabitur auctor est purus, ut rutrum enim vulputate id. Proin id urna elementum, accumsan quam sit amet, pulvinar quam. Duis porttitor dui hendrerit, laoreet mauris nec, efficitur tortor. Suspendisse potenti. Fusce eu feugiat ex, in pharetra tortor. Nunc quis tortor ligula. Nunc mattis odio dolor, commodo dapibus urna finibus non. Cras ac tortor eleifend, varius enim et, dignissim magna.",
"Vivamus vel orci sit amet turpis tincidunt viverra in in ipsum. Mauris in dolor id dui accumsan sodales at bibendum enim. Integer et tellus fermentum, egestas turpis in, hendrerit sapien. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Etiam vestibulum sapien ligula, at mollis dolor suscipit sed. Vivamus sapien lacus, pharetra nec sodales id, placerat sit amet quam. Donec posuere, arcu non vulputate luctus, mi nunc posuere magna, sit amet finibus metus mi nec sem. Nulla urna dui, vulputate sed facilisis sed, ullamcorper eget nulla. Aliquam porttitor ex nec sapien lobortis laoreet. Mauris imperdiet facilisis erat dictum tempor.",
"Phasellus risus enim, gravida eget imperdiet ut, laoreet nec magna. Ut pulvinar facilisis arcu in feugiat. Donec auctor non justo non suscipit. Integer faucibus lectus ut orci lobortis, ut cursus metus venenatis. Mauris vitae facilisis dolor, sit amet semper erat. Nunc id elit fringilla, accumsan lectus laoreet, tincidunt est. Nunc at dui quis tortor pulvinar ullamcorper efficitur id nulla. Curabitur ultrices euismod metus. Phasellus orci libero, vestibulum id venenatis id, fermentum luctus metus. Pellentesque in libero vitae sapien efficitur varius. Suspendisse non elementum ante, vel porttitor nibh. Nullam sed aliquam ipsum. Proin accumsan rutrum cursus. Nunc scelerisque, nisi sed aliquam laoreet, lorem nulla tristique lacus, quis varius est nunc vel eros. Mauris ultrices finibus risus, id viverra massa mattis vitae."
]

summary_urls = ["www.krinkle.com", "www.maggie.com", "www.zippy.com", "www.sue.com", "www.blackie.com"]

for i in range(len(summary_text)):
    article = Article(summary_text[i], summary_urls[i]) # query db and create instance of Article
    list_of_article_objects.append(article)

article0 = list_of_article_objects[1]

@app.route('/', methods=["GET", "POST"])
def home_page(): 
    possible_tags1 = ["Poverty", "Clean Water", "Malaria", "Children's Cancer", "Pet Rescue", "Global Warming", "Black Lives Matter", "Girls in Tech", "Veteren Affairs", "Police Violence"]
    possible_tags2 = ["Poverty", "Clean Water", "Malaria", "Children's Cancer", "Pet Rescue", "Global Warming", "Black Lives Matter", "Girls in Tech", "Veteren Affairs", "Police Violence"]    
    possible_tags3 = ["Poverty", "Clean Water", "Malaria", "Children's Cancer", "Pet Rescue", "Global Warming", "Black Lives Matter", "Girls in Tech", "Veteren Affairs", "Police Violence"]    

    url = request.form.get('id2')
    print "id2 =", url
    if url == None: 
        return render_template("index2.html", article=article0, first_tags = possible_tags1, second_tags = possible_tags2, third_tags = possible_tags3)
    else:
        article = next_article()
        return render_template("index2.html", article=article, first_tags = possible_tags1, second_tags = possible_tags2, third_tags = possible_tags3)

def next_article():
    # if 'next' is clicked
    print "I got clicked"
    url = request.form.get('name')
    print url
    tag_value = request.form.get('id')
    if tag_value != None:
        print "value =", tag_value
    if url != None:
        index = summary_urls.index(url)
        next_index = index + 1
        # new_url = summary_urls[next_index]
        article = list_of_article_objects[next_index]
        return article 




if __name__ == "__main__":
    app.run(debug = True)