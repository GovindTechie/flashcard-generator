# 🧠 Flashcard MCQ App with PDF Export

A simple and interactive Flashcard-based Multiple Choice Question (MCQ) web app built using **Flask**, enhanced with **NLP** capabilities using spaCy, and includes a one-click **PDF export** feature.

## 🚀 Features

- ✅ Create flashcards with questions and MCQ options.
- ✅ NLP-powered keyword highlighting.
- ✅ Instant feedback on correct/incorrect options.
- ✅ Responsive UI with color-coded flashcards.
- ✅ All content displayed on one page (no scrolling).
- ✅ One-click **Download as PDF** of all flashcards.
- ✅ Easy to deploy on Render or other cloud platforms.

## 🛠️ Built With

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [spaCy](https://spacy.io/) (for NLP tasks)
- [reportlab](https://www.reportlab.com/) (for PDF generation)
- HTML + CSS + JavaScript

## 📦 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/flashcard-mcq-app.git
    cd flashcard-mcq-app
    ```

2. **Create virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download spaCy model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

5. **Run the app locally:**
    ```bash
    python app.py
    ```

6. Open your browser and go to: [http://localhost:5000](http://localhost:5000)

## 🌐 Deployment (Render)

1. Make sure `gunicorn` is in your `requirements.txt`:
    ```txt
    gunicorn
    ```

2. Create a `render.yaml` or set the **Start Command** as:
    ```bash
    gunicorn app:app --bind 0.0.0.0:5000
    ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> Made with ❤️ by Govind Khedkar
