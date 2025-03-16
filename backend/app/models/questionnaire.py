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
DB_NAME = os.getenv('DB_NAME', 'questionnaire_db')

try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    questionnaire_collection = db['questionnaires']
    print(f"Successfully connected to MongoDB: {DB_NAME}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e

class QuestionnaireStatus(str, Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    STOPPED = "Stopped"
    COMPLETE = "Complete"

class QuestionBase(BaseModel):
    text: str
    type: str
    options: Optional[List[str]] = []

class Questionnaire(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    questions: List[QuestionBase]
    created_at: datetime = Field(default_factory=datetime.now)
    status: QuestionnaireStatus = QuestionnaireStatus.NOT_STARTED

    def to_mongo(self):
        """Convert to MongoDB document"""
        return {
            "_id": ObjectId(self.id) if not isinstance(self.id, ObjectId) else self.id,
            "title": self.title,
            "questions": [q.dict() for q in self.questions],
            "created_at": self.created_at,
            "status": self.status
        }

    @classmethod
    def from_mongo(cls, data):
        """Create instance from MongoDB document"""
        if data:
            data['id'] = str(data.pop('_id'))
            return cls(**data)
        return None 