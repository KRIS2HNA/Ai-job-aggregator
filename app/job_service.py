from sqlalchemy.exc import IntegrityError
from .database import SessionLocal
from .models import Job, Skill, JobSkill
from .scraper import scrape_jobs 
from .skill_extractor import extract_skills
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
