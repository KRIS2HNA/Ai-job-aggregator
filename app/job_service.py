from sqlalchemy.exc import IntegrityError
from .models import Job, Skill, JobSkill
import uuid

def create_job_eith_skills(db):
    try:
        job = Job( 
            title="AI Engineer",
            company="Google",
            Location="Bangalore",
            description="AI/ML role",
            apply_link=f"https://careers.google.com/jobs/results/{uuid.uuid4()}"
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
            link = JobSkill(job_id=job.id, skill_id=skill.id)
            db.add(link)
            
        db.commit()
        return {"message": "Job with skills added successfully"}
    
    except IntegrityError:
        db.rollback()
        return {"message": "Integrity error occurred"}
