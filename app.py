from flask import Flask, render_template, request
from flashcard_logic import generate_flashcards

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    flashcards = []
    if request.method == "POST":
        text = request.form["input_text"]
        flashcards = generate_flashcards(text)
    return render_template("index.html", flashcards=flashcards)

if __name__ == "__main__":
    app.run(debug=True)
