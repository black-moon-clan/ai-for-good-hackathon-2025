# Document Processing Pipeline Frontend

This is the frontend application for the Document Processing Pipeline. It allows users to configure and manage document processing tasks.

## Features

- Create and manage document processing tasks
- Configure source and destination settings
- Specify Google API credentials
- Start and monitor processing tasks

## Getting Started

### Prerequisites

- Node.js and npm

### Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

3. Build for production:
   ```
   npm run build
   ```

## Configuration

The application communicates with a Flask backend API. Make sure the backend is running and accessible at the correct URL.

By default, the application expects the API to be available at `/api`. You can modify the API base URL in the `.env` file if needed. 