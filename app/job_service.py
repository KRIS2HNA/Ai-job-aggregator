from sqlalchemy.exc import IntegrityError
from .database import SessionLocal
from .models import Job, Skill, JobSkill
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
