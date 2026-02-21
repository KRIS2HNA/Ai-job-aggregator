from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base
from .job_service import create_job_with_skills, get_all_jobs
from .schemas import JobResponse
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



    