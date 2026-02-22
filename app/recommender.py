from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_recommendations(jobs_data):
    """
    jobs_data = [{"id": 1, "skills": ["Python", "Machine Learning"]}, ...]
     
    """
    
    job_ids = []
    skill_strings = []
    
    for job in jobs_data:
        job_ids.append(job["id"])
        skill_strings.append(" ".join(job["skills"]))
        
    vectorizer = CountVectorizer()
    skill_matrix = vectorizer.fit_transform(skill_strings)
    
    similarity_matrix = cosine_similarity(skill_matrix)
    
    return job_ids, similarity_matrix

    