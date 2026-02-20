from pydantic import BaseModel
from typing import List

class JobResponse(BaseModel):
    title: str
    company: str
    location: str
    description: str
    source: str
    
    class Config:
        orm_model = True
        