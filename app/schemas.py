from pydantic import BaseModel
from typing import List

class JobResponse(BaseModel):
    title: str
    company: str
    location: str
    # description: str
    source: str
    
    class Config:
        orm_model = True
        
class JobDetailResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    apply_link: str
    skills: List[str]