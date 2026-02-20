from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base, Job, Skill, JobSkill
from sqlalchemy.exc import IntegrityError
import uuid


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}

# Create tables automatically
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Database connected and table created"}


@app.get("/add-test-job")
def add_test_job():
    db = SessionLocal()
    
    new_job = Job(
        title="Machine Learning Engineer",
        company="OpenAI"
    )
    
    db.add(new_job)
    db.commit()
    db.close()
    
    return {"message": "Test job inserted successfully"}

@app.get("/add-job-with-skills")
def add_job_with_skills():
    db = SessionLocal()

    # Create job (always new for testing)
    job = Job(
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

    # Create skills
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


    # Link job and skills
    for skill in skills:
        link = JobSkill(job_id=job.id, skills_id=skill.id)
        db.add(link)

    db.commit()
    db.close()

    return {"message": "Job with skills added successfully"}


@app.get("/jobs")
def get_jobs():
    db = SessionLocal()
    
    jobs = db.query(Job).distinct(Job.id).all()
    result = []
    
    for job in jobs:
        skill_list = []
        
        links = db.query(JobSkill).filter(JobSkill.job_id == job.id).all()
        
        for link in links:
            skill = db.query(Skill).filter(Skill.id == link.skills_id).first()
            
            if skill:
                skill_list.append(skill.name)
                
        result.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "skills": skill_list
        })
    
    db.close()
    return result