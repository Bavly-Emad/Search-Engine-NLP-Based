import time, sys, atexit
import sys
from flask import Flask, render_template, request, redirect,url_for
from flask_restful import Api, Resource

sys.path.append('app\search_engine')

try:
    from search_engine.utils.autoComplete import getSuggestions, saveQuery, saveAutoCompleteIndex
except:
    raise
Production = 1
#
if Production:
    from search_engine.Search import search

    print("search engine loaded")
else:
    docs = [{'_id': '1', 'imdb_id': 'tt0113497', 'original_title': 'Jumanji',
             'overview': "When siblings Judy and Peter discover an enchanted board game that opens the door to a magical world, they unwittingly invite Alan -- an adult who's been trapped inside the game for 26 years -- into their living room. Alan's only hope for freedom is to finish the game, which proves risky as all three find themselves running from giant rhinoceroses, evil monkeys and other terrifying creatures.",
             'poster_path': '/z46R8oShx61gXMrAmd7ptpVqNI0.jpg', 'release_date': '1995-12-15'}]


    def search(query, searchType):
        return docs

app = Flask(__name__)
api = Api(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True


class autocomplete(Resource):
    def get(self, query):
        suggestions = getSuggestions(query)
        return {"data": suggestions}

    def post(self, query):
        query = query.replace("-", " ")
        saveQuery(query)
        return {"data": "saved"}


api.add_resource(autocomplete, "/autocomplete/<string:query>")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Search", methods=["POST", "GET"])
def Search():
    start = time.time()

    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        query = request.form['search_box']
        searchType = request.form['select_box']
        docs = search(query, searchType)
        time_taken = time.time() - start
        return render_template('search.html', docs=docs, took=round(time_taken, 3))
@app.route("/Feedback",methods=["POST"])
def Feedback():
    return render_template("feedback.html")


if __name__ == '__main__':
    app.run(debug=True)
