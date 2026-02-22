import spacy 
from spacy.matcher import PhraseMatcher

#  load the spacy model
nlp = spacy.load("en_core_web_sm")

# skill dictionary (expandable)

SKILLS = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "TenserFlow",
    "PyTorch",
    "SQL",
    "AWS",
    "Docker",
    "Kubernetes",
    "Statistics",
    "Data Analysis",
    "Data Visualization",
    "Natural Language Processing",
    "Computer Vision",
    "Big Data",
    "Supervised Learning",
    "Unsupervised Learning"
]

#  create matcher

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS]
matcher.add("SKILLS", patterns)

def extract_skills(description: str):
    doc = nlp(description)
    matches = matcher(doc)
    
    extracted = set()
    
    for match_id, start, end in matches:
        skill = doc[start:end].text
        extracted.add(skill)
    return list(extracted)