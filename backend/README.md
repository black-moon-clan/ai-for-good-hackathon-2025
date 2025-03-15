# Document Processing Pipeline Backend

This is the backend API for the Document Processing Pipeline. It handles document processing tasks, including fetching files from Google Drive, processing them, and storing the results in Google Sheets or CSV files.

## Features

- RESTful API for managing document processing tasks
- Integration with Google Drive and Google Sheets
- Document processing pipeline
- MongoDB for task storage

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=document_processor
   PORT=5000
   ```

4. Run the application:
   ```
   python app.py
   ```

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/:taskId` - Get a specific task
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/:taskId` - Update a task
- `DELETE /api/tasks/:taskId` - Delete a task
- `POST /api/tasks/:taskId/start` - Start processing a task

## Google API Setup

To use this application, you'll need:

1. A Google Cloud Platform account
2. A project with the Google Drive API and Google Sheets API enabled
3. A service account with appropriate permissions
4. The service account credentials (JSON) 