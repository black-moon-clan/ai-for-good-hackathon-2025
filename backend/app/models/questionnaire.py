from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class QuestionBase(BaseModel):
    text: str
    type: str  # "multiple_choice" or "essay"
    options: Optional[List[str]] = []  # For multiple choice questions

class Questionnaire(BaseModel):
    title: str
    questions: List[QuestionBase]
    created_at: datetime = datetime.now() 