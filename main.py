import requests

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def show_word():
    if request.method == "POST":
        search_word = request.form.get("word")
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{search_word}"
        response = requests.get(url)
        data = response.json()

        try:
            if data["title"] == "No Definitions Found":
                print("no results")
                error_msg = f"Sorry there are no search results for the word: {search_word}"
                return render_template("index.html", error=error_msg)
        except TypeError:
            print("Search result is successful. You can ignore this error.")
            print("When search result is successful, data variable becomes a list.")
            print("Thus, data['title'] is an incorrect usage of list slicing and it causes TypeError.")

        # below is word definitions / all of them
        search_word_meanings = data[0]["meanings"]

        # noun definitions only
        noun_definitions_all = []

        try:
            noun_def = search_word_meanings[0]["definitions"]
        except IndexError:
            print("This word doesn't have a noun definition")
            noun_definitions_all = "None"
        else:
            for defi in noun_def:
                noun_definitions_all.append(defi["definition"])

        # verb definitions only
        verb_definitions_all = []

        try:
            verb_def = search_word_meanings[1]["definitions"]
        except IndexError:
            print("This word doesn't have a verb definition")
            verb_definitions_all = "None"
        else:
            for defi in verb_def:
                verb_definitions_all.append(defi["definition"])

        return render_template(
            "index.html",
            word=search_word,
            noun_definition=noun_definitions_all,
            verb_definition=verb_definitions_all,
            searched=True
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="localhost")
