from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from enum import Enum

def generate_uuid():
    return str(uuid.uuid4())

class QuestionnaireStatus(str, Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    STOPPED = "Stopped"
    COMPLETE = "Complete"

class QuestionBase(BaseModel):
    text: str
    type: str  # "rating" or "open_ended"
    options: Optional[List[str]] = []  # For rating questions

class Questionnaire(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    title: str
    questions: List[QuestionBase]
    created_at: datetime = datetime.now()
    status: QuestionnaireStatus = QuestionnaireStatus.NOT_STARTED 