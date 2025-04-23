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

    answers_summary = []

    for idx, card in enumerate(flashcards, start=1):
        p.drawString(40, y, f"{idx}. {card['question']}")
        y -= 15
        for i, opt in enumerate(card['options']):
            label = chr(97 + i)
            p.drawString(60, y, f"{label}) {opt}")
            y -= 12
        answers_summary.append(f"{idx}. {card['answer']}")
        y -= 10

        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

    # Add a new page for answers, start high enough to fit all
    p.showPage()
    p.setFont("Helvetica-Bold", 12)
    p.drawString(width - 200, height - 60, "Answers:")
    p.setFont("Helvetica", 10)

    answer_start_y = height - 80
    for i, ans in enumerate(answers_summary):
        p.drawRightString(width - 40, answer_start_y - i * 14, ans)

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
