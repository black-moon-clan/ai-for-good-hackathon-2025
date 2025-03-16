from app.config import tasks_collection
from app.models.task import Task
from bson import ObjectId
import threading
import time
import json
import os
import requests
import tempfile

# Import Google API libraries conditionally to avoid errors if not installed
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2 import service_account
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False
    print("Google API libraries not available. Some features will be limited.")

SERVICE_ACCOUNT_FILE = "config/service_account.json"

class TaskService:
    @staticmethod
    def get_all_tasks():
        try:
            # Try MongoDB-style sorting
            tasks = list(tasks_collection.find().sort('createdAt', -1))
        except TypeError:
            # Fallback for in-memory store
            tasks = list(tasks_collection.find())
            # Sort manually by createdAt if available
            tasks.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        return [Task.from_dict(task).to_dict() for task in tasks]
    
    @staticmethod
    def get_task_by_id(task_id):
        task = tasks_collection.find_one({'_id': task_id})
        if task:
            return Task.from_dict(task).to_dict()
        return None
    
    @staticmethod
    def create_task(task_data):
        task = Task.from_dict(task_data)
        result = tasks_collection.insert_one(task.to_dict())
        return task.to_dict()
    
    @staticmethod
    def update_task(task_id, task_data):
        existing_task = tasks_collection.find_one({'_id': task_id})
        if not existing_task:
            return None
        
        # Preserve the _id and createdAt fields
        task_data['_id'] = task_id
        task_data['createdAt'] = existing_task.get('createdAt')
        
        updated_task = Task.from_dict(task_data)
        tasks_collection.update_one(
            {'_id': task_id},
            {'$set': updated_task.to_dict()}
        )
        return updated_task.to_dict()
    
    @staticmethod
    def delete_task(task_id):
        result = tasks_collection.delete_one({'_id': task_id})
        return result.deleted_count > 0
    
    @staticmethod
    def start_task(task_id):
        task = tasks_collection.find_one({'_id': task_id})
        if not task:
            return False
        
        # Update task status to in_progress
        tasks_collection.update_one(
            {'_id': task_id},
            {'$set': {'status': 'in_progress'}}
        )
        
        # Start processing in a separate thread
        thread = threading.Thread(
            target=TaskService._process_task,
            args=(task,)
        )
        thread.daemon = True
        thread.start()
        
        return True
    
    @staticmethod
    def _process_task(task):
        try:
            # Convert task dictionary to Task object
            task_obj = Task.from_dict(task)
            
            # Process files from Google Drive
            if task_obj.source_type == 'google_drive':
                if not GOOGLE_APIS_AVAILABLE:
                    # Simulate processing if Google APIs are not available
                    time.sleep(2)
                    results = [
                        {
                            'filename': 'sample_document_1.jpg',
                            'content': TaskService._process_file_with_external_api(None)
                        },
                        {
                            'filename': 'sample_document_2.jpg',
                            'content': TaskService._process_file_with_external_api(None)
                        }
                    ]
                else:
                    # Get files from Google Drive
                    files = TaskService._get_files_from_google_drive(task_obj)
                    
                    # Process each file
                    results = []
                    for file in files:
                        # Download the file
                        file_content = TaskService._download_file(file, task_obj)
                        
                        # Process the file using external API
                        processed_content = TaskService._process_file_with_external_api(file_content)
                        
                        # Add to results
                        results.append({
                            'filename': file['name'],
                            'content': processed_content
                        })
                
                # Save results to output destination
                if task_obj.output_type == 'google_sheets':
                    if GOOGLE_APIS_AVAILABLE:
                        TaskService._save_to_google_sheets(results, task_obj)
                    else:
                        print(f"Would save to Google Sheets: {results}")
                elif task_obj.output_type == 'csv':
                    TaskService._save_to_csv(results, task_obj)
            
            # Update task status to completed
            tasks_collection.update_one(
                {'_id': task_obj._id},
                {'$set': {'status': 'completed'}}
            )
            
        except Exception as e:
            print(f"Error processing task: {str(e)}")
            # Update task status to failed
            tasks_collection.update_one(
                {'_id': task['_id']},
                {'$set': {'status': 'failed'}}
            )
    
    @staticmethod
    def _get_files_from_google_drive(task):
        if not GOOGLE_APIS_AVAILABLE:
            return []
            
        # Parse Google credentials
        credentials_info = SERVICE_ACCOUNT_FILE
        credentials = service_account.Credentials.from_service_account_file(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        # Build the Drive API client
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # List files in the specified folder
        results = drive_service.files().list(
            q=f"'{task.source_path}' in parents and mimeType contains 'application/pdf'",
            fields="files(id, name, mimeType)"
        ).execute()
        
        return results.get('files', [])
    
    @staticmethod
    def _download_file(file, task):
        if not GOOGLE_APIS_AVAILABLE:
            return None
            
        # Parse Google credentials
        credentials_info = json.loads(task.google_credentials)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        # Build the Drive API client
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Download the file
        request = drive_service.files().get_media(fileId=file['id'])
        
        # Create a temporary file to store the downloaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            downloader = MediaFileUpload(temp_file.name, resumable=True)
            downloader.resumable_progress = 0
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            # Return the path to the temporary file
            return temp_file.name
    
    @staticmethod
    def _process_file_with_external_api(file_path):
        # This is a placeholder for the external API call
        # In a real implementation, you would send the file to an OCR or document processing API
        # For demonstration purposes, we'll just return some dummy data
        
        # Simulate API processing time
        time.sleep(2)
        
        # Return dummy data
        return {
            "text": "This is extracted text from the document.",
            "fields": {
                "name": "John Doe",
                "date": "2023-01-15",
                "address": "123 Main St, Anytown, USA"
            }
        }
    
    @staticmethod
    def _save_to_google_sheets(results, task):
        if not GOOGLE_APIS_AVAILABLE:
            return
            
        # Parse Google credentials
        credentials_info = json.loads(task.google_credentials)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build the Sheets API client
        sheets_service = build('sheets', 'v4', credentials=credentials)
        
        # Check if the spreadsheet exists, if not create it
        spreadsheet_id = task.output_path
        if not spreadsheet_id or spreadsheet_id == "":
            # Create a new spreadsheet
            spreadsheet = sheets_service.spreadsheets().create(
                body={
                    'properties': {'title': f"Document Processing Results - {task.name}"}
                }
            ).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']
            
            # Update the task with the new spreadsheet ID
            tasks_collection.update_one(
                {'_id': task._id},
                {'$set': {'outputPath': spreadsheet_id}}
            )
        
        # Prepare data for the spreadsheet
        values = [
            ["Filename", "Name", "Date", "Address", "Full Text"]
        ]
        
        for result in results:
            values.append([
                result['filename'],
                result['content']['fields'].get('name', ''),
                result['content']['fields'].get('date', ''),
                result['content']['fields'].get('address', ''),
                result['content']['text']
            ])
        
        # Update the spreadsheet
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()
    
    @staticmethod
    def _save_to_csv(results, task):
        # Create CSV content
        csv_content = "Filename,Name,Date,Address,Full Text\n"
        
        for result in results:
            csv_content += f"{result['filename']},"
            csv_content += f"{result['content']['fields'].get('name', '')},"
            csv_content += f"{result['content']['fields'].get('date', '')},"
            csv_content += f"{result['content']['fields'].get('address', '')},"
            csv_content += f"{result['content']['text']}\n"
        
        # Write to file
        with open(task.output_path, 'w') as f:
            f.write(csv_content) 