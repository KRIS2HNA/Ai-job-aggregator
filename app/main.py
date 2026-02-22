from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base, Job
from .job_service import create_job_with_skills, get_all_jobs
from .schemas import JobResponse, JobDetailResponse
from typing import List
from .job_service import ingest_scraped_jobs


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.get("/add-job-with-skills")
def add_job():
    db = SessionLocal()
    response = create_job_with_skills(db)
    db.close()
    return response


@app.get("/jobs")
def get_jobs(
    location: str = None,
    skill: str = None,
    skip: int = 0,
    limit: int = 10
):    
    
    db = SessionLocal()
    jobs = get_all_jobs(db, location, skill, skip, limit  )
    db.close()
    return jobs

@app.get("/scrape")
def scrape_and_store():
    db = SessionLocal()
    result = ingest_scraped_jobs(db)
    db.close()
    return result


@app.get("/jobs/{job_id}", response_model = JobDetailResponse)
def get_job_detail(job_id: int):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        db.close()
        return {"error": "Job not found"}
    
    skill_names = [js.skill.name for js in job.job_skills]
    
    result = JobDetailResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        apply_link=job.apply_link,
        skills=skill_names
    )
    db.close()
    return result