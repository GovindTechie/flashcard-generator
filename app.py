from flask import Flask, render_template, request, session, send_file
from flashcard_logic import generate_flashcards
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-random-key'

@app.route("/", methods=["GET", "POST"])
def index():
    flashcards = []
    if request.method == "POST":
        text = request.form["input_text"]
        difficulty = request.form.get("difficulty", "medium")
        flashcards = generate_flashcards(text, difficulty)
        session['flashcards'] = flashcards
    else:
        session.pop('flashcards', None)
    return render_template("index.html", flashcards=flashcards)

@app.route("/download")
def download():
    flashcards = session.get('flashcards', [])
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    p.setFont("Helvetica", 10)

    for idx, card in enumerate(flashcards, start=1):
        # Write question
        q = f"{idx}. {card['question']}"
        p.drawString(40, y, q)
        y -= 15
        # Write options a), b), c)…
        for i, opt in enumerate(card['options']):
            label = chr(97 + i)  # 97='a'
            p.drawString(60, y, f"{label}) {opt}")
            y -= 12
        y -= 10
        # New page if needed
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

    p.save()
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="flashcards.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
