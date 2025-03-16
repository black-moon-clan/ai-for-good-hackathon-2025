from datetime import datetime

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

class SurveyService:
   
    @staticmethod
    def create_survey(survey_data):
        now = datetime.now() # current date and time

        data_to_append = [
            [now.strftime("%m/%d/%Y %H:%M:%S"), survey_data['firstName'], survey_data['lastName'], survey_data['improved_english_rating'], survey_data['confidence_rating']]
        ]
    
        SurveyService._append_data_to_google_sheets(data_to_append)
        return survey_data
    
    @staticmethod
    def _append_data_to_google_sheets(values):
        if not GOOGLE_APIS_AVAILABLE:
            return
            
        # Parse Google credentials
        SERVICE_ACCOUNT_FILE = "config/service_account.json"
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build the Sheets API client
        sheets_service = build('sheets', 'v4', credentials=credentials)

        SPREADSHEET_ID = "1OZqC_K0AHa1iuG0-SOaMUkEX44nmqtMRCwzizf6woKg"
        RANGE = "Reporting!A1"
        
        body = {"values": values}
        
        # Update the spreadsheet
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
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