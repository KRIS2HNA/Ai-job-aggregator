from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_embeddings(target_text, all_texts):
    # return model.encode(text_list)
    # compute embeddings
    
    embeddings = model.encode([target_text] + all_texts)
    
    target_vec = embeddings[0]
    doc_vecs = embeddings[1:]
    
    scores = cosine_similarity([target_vec], doc_vecs)[0]
    
    return scores

def semantic_similarity(query, documents):
    query_vec = model.encode([query])
    doc_vecs = model.encode(documents)
    
    scores = cosine_similarity(query_vec, doc_vecs)[0]
    
    return scores