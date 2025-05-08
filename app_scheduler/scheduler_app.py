import os
from flask import Blueprint, render_template, request, jsonify
from datetime import timedelta, datetime # Import datetime
import dateparser # Import dateparser

# Import Google API client libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Initialize a Blueprint for the scheduler module
# The url_prefix will be set when registering with the main app
scheduler_bp = Blueprint('scheduler', __name__,
                         template_folder='templates',
                         static_folder='static')

# Note: Secret key is configured in the main app, not here for a Blueprint

# --- Google Calendar Integration ---
# Handles Google OAuth flow and event creation.
def get_google_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ensure client_secret.json is in the project root
            client_secrets_file = os.getenv('GOOGLE_CLIENT_SECRETS_FILE', 'client_secret.json')
            if not os.path.exists(client_secrets_file):
                 print(f"Error: {client_secrets_file} not found. Please download it from Google Cloud Console.")
                 return None # Indicate failure to get service

            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            # This flow is typically for a desktop app. For a web app,
            # the redirect URI and flow would be different.
            # Since this is a backend service, a headless flow might be needed
            # or the user needs to run an initial script to generate token.json.
            # For simplicity here, we assume token.json is generated.
            print("Authorization required. Please run the Google Calendar quickstart to generate token.json.")
            return None # Indicate authorization is needed

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f'An API error occurred: {error}')
        return None

def create_google_calendar_event(task_description, start_time_str, end_time_str):
    """
    Creates a Google Calendar event.
    Requires Google Calendar API setup and authentication.
    """
    service = get_google_calendar_service()
    if not service:
        return {"status": "error", "message": "Google Calendar service not available. Check credentials and token.json."}

    try:
        # Convert ISO 8601 strings back to datetime objects if necessary,
        # or ensure they are in the correct format for the API.
        # The API expects 'YYYY-MM-DDTHH:mm:ssZ' or 'YYYY-MM-DDTHH:mm:ss+/-hh:mm'
        # dateparser.parse returns timezone-aware datetime objects, isoformat() is suitable.

        event = {
            'summary': task_description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': 'UTC', # Ensure this matches your dateparser settings or desired timezone
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'UTC', # Ensure this matches your dateparser settings or desired timezone
            },
        }

        # 'primary' refers to the user's default calendar
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return {"status": "success", "message": f"Directive logged: '{task_description}'. Event Link: {event.get('htmlLink')}"}

    except HttpError as error:
        print(f'An API error occurred: {error}')
        return {"status": "error", "message": f"Chrono-Sync Failed: Google Calendar API error - {error}"}
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return {"status": "error", "message": f"Chrono-Sync Failed: An unexpected error occurred - {e}"}


# --- Routes ---
@scheduler_bp.route('/')
def index():
    """
    Renders the main HTML page for the scheduler application (to be embedded in iframe).
    This route is relative to the blueprint's url_prefix ('/scheduler').
    """
    return render_template('scheduler_index.html')

@scheduler_bp.route('/log_task', methods=['POST'])
def log_task():
    """
    Receives natural language task description and attempts to schedule it.
    """
    data = request.get_json()
    task_input = data.get('task_input', '').strip()

    if not task_input:
        return jsonify({"status": "error", "message": "Directive input empty. Access Denied."}), 400

    # --- Natural Language Parsing ---
    # Implement dateparser logic here
    # Example using dateparser (install with: pip install dateparser)
    settings = {'RETURN_AS_TIMEZONE_AWARE': True, 'TIMEZONE': 'UTC'} # Adjust timezone as needed
    parsed_date = dateparser.parse(task_input, settings=settings)
    if parsed_date:
        # Attempt to extract duration or end time
        start_time = parsed_date
        # For simplicity, setting a default end time 1 hour after start
        # A more advanced implementation would parse duration from task_input
        end_time = start_time + timedelta(hours=1)
        task_description = task_input # Refine description extraction if needed
        result = create_google_calendar_event(task_description, start_time.isoformat(), end_time.isoformat())
    else:
        result = {"status": "error", "message": "Chrono-Sync Failed: Unable to parse directive."}

    return jsonify(result)

# This __main__ block is removed as the module will be run via the main app.