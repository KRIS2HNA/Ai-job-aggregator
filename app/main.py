from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base, Job, Skill, JobSkill
from sqlalchemy.exc import IntegrityError

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
    
    # Create a new job
    try:
        job = Job(
            title = "AI Engineer",
            company = "Google",
            location = "Bangalore",
            description = "AI/ML role",
            apply_link = "https://google.com/careers/ai-engineer-1",
            source = "Google Careers"
        )
    
        db.add(job) 
        db.commit()
        db.refresh(job)
    except IntegrityError:
        db.rollback()
        db.close()
        return {"message": "Job with this apply_link already exists"}

    
    # step 2: create skills
    skill_names = ["Python", "Machine Learning", "Deep Learning"]
    
    skills = []
    for name in skill_names:
        new_skill = Skill(name=name)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        skills.append(new_skill)
        
    # step 3: link job and skills
    
    for s in skills:
        link = JobSkill(job_id = job.id, skill_id= s.id)
        db.add(link)
        
    db.commit()
    db.close()
    
    return {"message": "job with skills added successfully"}