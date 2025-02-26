import os
import torch
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load BERT-based model for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")  # Load small Spacy model for NER

def calculate_resume_score(resume_text, job_description):
    """Calculate resume-job similarity using BERT, TF-IDF, and Named Entity Recognition (NER)."""
    
    # ✅ Step 1: BERT-based semantic similarity
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()

    # ✅ Step 2: TF-IDF keyword matching
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text, job_description])
    tfidf_similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]

    # ✅ Step 3: Named Entity Recognition (NER) for skill & experience matching
    resume_entities = extract_named_entities(resume_text)
    job_entities = extract_named_entities(job_description)
    entity_overlap = len(resume_entities & job_entities) / max(len(job_entities), 1)
    
    # ✅ Weighted scoring: Adjusting weights based on importance
    final_score = (similarity_score * 0.4 + tfidf_similarity * 0.3 + entity_overlap * 0.3) * 100
    
    return round(final_score, 2)

def extract_named_entities(text):
    """Extract named entities (skills, job titles, organizations) from text using Spacy."""
    doc = nlp(text)
    entities = {ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "NORP", "WORK_OF_ART", "PRODUCT"]}
    return entities

def generate_feedback(resume_text, job_description):
    """Generate keyword-based feedback for resume improvement."""
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    missing_keywords = job_words - resume_words
    feedback = f"Consider adding these keywords to your resume: {', '.join(missing_keywords)}"
    return feedback if missing_keywords else "Your resume aligns well with the job description!"
