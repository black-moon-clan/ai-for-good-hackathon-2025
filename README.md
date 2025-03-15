# Document Processing Pipeline

A full-stack application for processing documents from Google Drive and extracting their content into Google Sheets.

## Overview

This application allows users to:
1. Configure document processing tasks
2. Connect to their Google Drive to access documents
3. Process documents using AI/OCR technology
4. Store the extracted data in Google Sheets

## Project Structure

- `fe/` - React frontend application
- `backend/` - Flask backend API

## Getting Started

### Prerequisites

- Node.js and npm for the frontend
- Python 3.8+ for the backend
- MongoDB for data storage
- Google Cloud Platform account with API access

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd fe
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=document_processor
   PORT=5000
   ```

5. Run the application:
   ```
   python app.py
   ```

## Usage

1. Open the frontend application in your browser (default: http://localhost:3000)
2. Create a new task
3. Configure the task with your Google Drive folder and Google Sheets destination
4. Start the task
5. Monitor the task status and view results in your Google Sheets

## Google API Setup

To use this application, you'll need:

1. A Google Cloud Platform account
2. A project with the Google Drive API and Google Sheets API enabled
3. A service account with appropriate permissions
4. The service account credentials (JSON)
