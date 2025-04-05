import spacy
import random
import json

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

def generate_flashcards(text, difficulty="medium", num_choices=4):
    doc = nlp(text)
    flashcards = []
    for sent in doc.sents:
        if sent.ents:
            chosen_ent = random.choice(sent.ents)
            qword = entity_question_map.get(chosen_ent.label_, random.choice(default_question_words))
            question_sentence = sent.text.replace(chosen_ent.text, "_____")
            options = generate_choices(chosen_ent.text, doc, num_choices)
            flashcards.append({
                "question": f"{qword}: {question_sentence}",
                "answer": chosen_ent.text,
                "options": options
            })
        else:
            tokens = [token for token in sent if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"]]
            if tokens:
                chosen = random.choice(tokens)
                question_sentence = sent.text.replace(chosen.text, "_____")
                options = generate_choices(chosen.text, doc, num_choices)
                flashcards.append({
                    "question": f"What: {question_sentence}",
                    "answer": chosen.text,
                    "options": options
                })
    return flashcards

def generate_choices(correct_answer, doc, num_choices=4):
    words = list(set([ent.text for ent in doc.ents if ent.text != correct_answer]))
    if len(words) < num_choices - 1:
        words.extend([token.text for token in doc if token.is_alpha and token.text != correct_answer])
    words = list(set(words))
    if len(words) < num_choices - 1:
        distractors = words
    else:
        distractors = random.sample(words, num_choices - 1)
    choices = distractors + [correct_answer]
    random.shuffle(choices)
    return choices
