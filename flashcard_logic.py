import spacy
import random

nlp = spacy.load("en_core_web_sm")

entity_question_map = {
    "PERSON": "Who",
    "GPE": "Where",
    "LOC": "Where",
    "DATE": "When",
    "TIME": "When",
    "ORG": "Which organization",
    "MONEY": "How much",
    "PERCENT": "What percentage",
    "EVENT": "Which event",
    "WORK_OF_ART": "Which work of art",
    "LAW": "Which law",
    "PRODUCT": "Which product"
}

default_question_words = ["What", "Which", "Why", "How"]

def generate_flashcards(text, difficulty="medium"):
    if difficulty.lower() == "easy":
        num_choices = 3
    elif difficulty.lower() == "hard":
        num_choices = 6
    else:
        num_choices = 4

    doc = nlp(text)
    flashcards = []
    used_answers = set()

    for sent in doc.sents:
        if sent.ents:
            ents = [ent for ent in sent.ents if ent.text.lower() not in used_answers]
            if not ents:
                continue
            chosen_ent = random.choice(ents)
            used_answers.add(chosen_ent.text.lower())
            qword = entity_question_map.get(chosen_ent.label_, random.choice(default_question_words))
            question_sentence = sent.text.replace(chosen_ent.text, "_____ ", 1)
            options = generate_choices(chosen_ent.text, doc, num_choices)
            full_question = f"{qword} {question_sentence}" if qword != "When" else question_sentence
            flashcards.append({
                "question": full_question.strip(),
                "answer": chosen_ent.text,
                "options": options
            })
        else:
            tokens = [token for token in sent if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"] and token.text.lower() not in used_answers]
            if tokens:
                chosen = random.choice(tokens)
                used_answers.add(chosen.text.lower())
                question_sentence = sent.text.replace(chosen.text, "_____ ", 1)
                options = generate_choices(chosen.text, doc, num_choices)
                flashcards.append({
                    "question": question_sentence.strip(),
                    "answer": chosen.text,
                    "options": options
                })

    return flashcards

def generate_choices(correct_answer, doc, num_choices=4):
    correct_lower = correct_answer.lower()
    distractors = list({ent.text for ent in doc.ents if ent.text.lower() != correct_lower})
    
    if len(distractors) < num_choices - 1:
        distractors.extend([token.text for token in doc if token.is_alpha and token.text.lower() != correct_lower])

    distractors = list(set(distractors))
    selected_distractors = random.sample(distractors, min(len(distractors), num_choices - 1))
    
    choices = selected_distractors + [correct_answer]
    random.shuffle(choices)
    return choices
