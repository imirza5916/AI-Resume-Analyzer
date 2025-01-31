import spacy
import re

def load_nlp_model():
    """Load spaCy NLP model with custom rules for extracting resume information."""
    nlp = spacy.load("en_core_web_sm")

    # Add custom entity recognition patterns
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "SKILLS", "pattern": "Python"},
        {"label": "SKILLS", "pattern": "Java"},
        {"label": "EDUCATION", "pattern": "Bachelor of Science"},
        {"label": "EDUCATION", "pattern": "Computer Science"},
        {"label": "JOB_TITLE", "pattern": "Software Engineer"}
    ]
    ruler.add_patterns(patterns)
    
    return nlp

def extract_resume_info(resume_text):
    """Extract structured resume information using NLP."""
    nlp = load_nlp_model()
    doc = nlp(resume_text)

    extracted_data = {
        "SKILLS": [],
        "EDUCATION": [],
        "ORG": [],
        "JOB_TITLE": []
    }

    for ent in doc.ents:
        if ent.label_ in extracted_data:
            extracted_data[ent.label_].append(ent.text)

    # Remove duplicates and clean data
    for key in extracted_data:
        extracted_data[key] = list(set(extracted_data[key]))

    return extracted_data

if __name__ == "__main__":
    with open("resume_text.txt", "r", encoding="utf-8") as file:
        resume_text = file.read()

    extracted_info = extract_resume_info(resume_text)
    print("\n🔹 Extracted Resume Information:")
    for key, value in extracted_info.items():
        print(f"{key}: {', '.join(value) if value else 'None Found'}")