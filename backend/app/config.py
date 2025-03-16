import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if we should use MongoDB or in-memory store
USE_MONGODB = os.environ.get('USE_MONGODB', 'false').lower() == 'true'

if USE_MONGODB:
    # MongoDB configuration
    from pymongo import MongoClient
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.environ.get('DB_NAME', 'document_processor')

    # Initialize MongoDB client
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Collections
    tasks_collection = db.tasks
else:
    # In-memory store for development
    class InMemoryCollection:
        def __init__(self):
            self.data = {}
            self.counter = 0
        
        def find(self):
            return self
        
        def find_one(self, query):
            _id = query.get('_id')
            return self.data.get(_id)
        
        def insert_one(self, document):
            _id = document.get('_id')
            self.data[_id] = document
            self.counter += 1
            return type('obj', (object,), {'inserted_id': _id})
        
        def update_one(self, query, update):
            _id = query.get('_id')
            if _id in self.data:
                if '$set' in update:
                    for key, value in update['$set'].items():
                        self.data[_id][key] = value
                return type('obj', (object,), {'modified_count': 1})
            return type('obj', (object,), {'modified_count': 0})
        
        def delete_one(self, query):
            _id = query.get('_id')
            if _id in self.data:
                del self.data[_id]
                return type('obj', (object,), {'deleted_count': 1})
            return type('obj', (object,), {'deleted_count': 0})
        
        def sort(self, *args, **kwargs):
            # Just return self for chaining, actual sorting will be done when converted to list
            return self
        
        def __iter__(self):
            # Return all values in the data dictionary
            return iter(self.data.values())
    
    # Create in-memory collections
    tasks_collection = InMemoryCollection()
    
    print("Using in-memory store instead of MongoDB") 