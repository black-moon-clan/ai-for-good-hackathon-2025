from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class QuestionBase(BaseModel):
    text: str
    type: str  # "multiple_choice" or "essay"
    options: Optional[List[str]] = []  # For multiple choice questions

class Questionnaire(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    title: str
    questions: List[QuestionBase]
    created_at: datetime = datetime.now() 