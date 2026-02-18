from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base, Job

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