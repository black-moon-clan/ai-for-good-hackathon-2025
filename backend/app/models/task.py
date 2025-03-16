from datetime import datetime
from bson import ObjectId

class Task:
    def __init__(self, name, source_type='google_drive', source_path='', 
                 output_type='google_sheets', output_path='', 
                 google_api_key='', google_credentials='', 
                 status='pending', _id=None, created_at=None):
        self._id = _id or str(ObjectId())
        self.name = name
        self.source_type = source_type
        self.source_path = source_path
        self.output_type = output_type
        self.output_path = output_path
        self.google_api_key = google_api_key
        self.google_credentials = google_credentials
        self.status = status
        self.created_at = created_at or datetime.utcnow().isoformat()
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name', 'New Task'),
            source_type=data.get('sourceType', 'google_drive'),
            source_path=data.get('sourcePath', ''),
            output_type=data.get('outputType', 'google_sheets'),
            output_path=data.get('outputPath', ''),
            google_api_key=data.get('googleApiKey', ''),
            google_credentials=data.get('googleCredentials', ''),
            status=data.get('status', 'pending'),
            _id=data.get('_id'),
            created_at=data.get('createdAt')
        )
    
    def to_dict(self):
        return {
            '_id': self._id,
            'name': self.name,
            'sourceType': self.source_type,
            'sourcePath': self.source_path,
            'outputType': self.output_type,
            'outputPath': self.output_path,
            'googleApiKey': self.google_api_key,
            'googleCredentials': self.google_credentials,
            'status': self.status,
            'createdAt': self.created_at
        } 