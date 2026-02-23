from sqlalchemy.exc import IntegrityError
from .database import SessionLocal
from .models import Job, Skill, JobSkill
from .scraper import scrape_jobs 
from .skill_extractor import extract_skills
from sqlalchemy import func
from .recommender import build_recommendations

import uuid

def create_job_with_skills(db):
    db = SessionLocal()
    try:
        job = Job ( 
            title="AI Engineer",
            company="Google",
            location="Bangalore",
            description="AI/ML role",
            apply_link=f"https://careers.google.com/jobs/results/{uuid.uuid4()}",
            source="Google Careers"
        )
        
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        skill_names = ["Python", "Machine Learning", "Deep Learning"]
        skills = []
        
        for name in skill_names:
            skill = db.query(Skill).filter(Skill.name == name).first()
            
            if not skill:
                skill = Skill(name=name)
                db.add(skill)
                db.commit()
                db.refresh(skill)
                
            skills.append(skill)
            
        for skill in skills:
            link = JobSkill(job=job, skill=skill)
            db.add(link)
            
        db.commit()
        return {"message": "Job with skills added successfully"}
    
    except IntegrityError:
        db.rollback()
        return {"message": "Integrity error occurred"}
def get_all_jobs(db, location, skill, skip, limit):
    jobs = db.query(Job)
    if location:
        jobs = jobs.filter(Job.location == location)
    if skill:
        jobs = jobs.join(JobSkill).join(Skill).filter(Skill.name == skill)
    jobs = jobs.offset(skip).limit(limit).all()
    result = []
    
    for job in jobs:
        skill_links = db.query(JobSkill).filter(JobSkill.job_id == job.id).all()
        skill_names = []
        
        for link in skill_links:
            skill = db.query(Skill).filter(Skill.id == link.skill_id).first()
            if skill:
                skill_names.append(skill.name)
                
        result.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "apply_link": job.apply_link,
            "source": job.source,
            "skills": skill_names
        })
        
    return result

def ingest_scraped_jobs(db):
    scraped_jobs = scrape_jobs()
    
    for job_data in scraped_jobs:
        
        # check if job already exists 
        existing_job = db.query(Job).filter(
            Job.apply_link == job_data["apply_link"]
        ).first()
        if existing_job:
            continue
        
        # Create Job
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            description=job_data["description"],
            apply_link=job_data["apply_link"],
            source="Scraped Data"
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        description = job_data.get("description", "")
        extracted_skills = extract_skills(description)
        
        # Add skills(get or create)
        for skill_name in extracted_skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
                db.commit()
                db.refresh(skill)
        
            # Link job and skill
            link = JobSkill(job = job, skill= skill)
            db.add(link)
        
        db.commit()
    
    return {"message": "Scraped jobs ingested successfully"}

def get_top_skills(db, limit=10):
    results = (
        db.query(Skill.name, func.count(JobSkill.job_id).label("job_count"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .group_by(Skill.name)
        .order_by(func.count(JobSkill.job_id).desc())
        .limit(limit)
        .all()
    )
    
    return [{"skill": name, "job_count": job_count} for name, job_count in results]


def get_top_locations(db, limit=10):
    results = (
        db.query(Job.location, func.count(Job.id).label("job_count"))
        .group_by(Job.location)
        .order_by(func.count(Job.id).desc())
        .limit(limit)
        .all()
    )
    return [{"location": location, "job_count": job_count} for location, job_count in results]

def get_top_companies(db, limit=10):
    results = (
        db.query(Job.company, func.count(Job.id).label("job_count"))
        .group_by(Job.company)
        .order_by(func.count(Job.id).desc())
        .limit(limit)
        .all()
    )
    return [{"company": company, "job_count": job_count} for company, job_count in results] 



def get_recommendations(db, job_id, limit=5):

    jobs = db.query(Job).all()

    jobs_data = [] 

    for job in jobs:
        skills = [js.skill.name for js in job.job_skills]
        jobs_data.append({
            "id": job.id,
            "skills": skills
        })

    job_ids, similarity_matrix = build_recommendations(jobs_data)

    if job_id not in job_ids:
        return []

    index = job_ids.index(job_id)

    similarity_scores = list(enumerate(similarity_matrix[index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Skip itself (first one)
    top_similar = similarity_scores[1:6]

    recommendations = []

    for idx, score in top_similar:
        recommendations.append(jobs_data[idx]["id"])

    return recommendations

