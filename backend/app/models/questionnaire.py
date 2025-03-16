from datetime import datetime
from typing import List, Optional
from enum import Enum
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection setup
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')

# In-memory fallback storage
questionnaires = []  # Add this line to export the fallback storage

try:
    client = MongoClient(MONGODB_URI)
    db = client['questionnaire_db']
    questionnaire_collection = db['questionnaires']
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Warning: Could not connect to MongoDB. Using in-memory store instead. Error: {e}")

class QuestionnaireStatus(str, Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    STOPPED = "Stopped"
    COMPLETE = "Complete"

class QuestionBase(BaseModel):
    text: str
    type: str  # "rating" or "open_ended"
    options: Optional[List[str]] = []

class Questionnaire(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    questions: List[QuestionBase]
    created_at: datetime = Field(default_factory=datetime.now)
    status: QuestionnaireStatus = QuestionnaireStatus.NOT_STARTED

    def to_mongo(self):
        return {
            "_id": ObjectId(self.id) if not isinstance(self.id, ObjectId) else self.id,
            "title": self.title,
            "questions": [q.dict() for q in self.questions],
            "created_at": self.created_at,
            "status": self.status
        }

    @classmethod
    def from_mongo(cls, data):
        if data:
            data['id'] = str(data.pop('_id'))
            return cls(**data)
        return None 