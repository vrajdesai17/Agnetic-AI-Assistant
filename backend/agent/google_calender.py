import datetime
import os
import pickle
from pytz import timezone
import re

# It's used for handling OAuth 2.0 authorization when your app needs to access Google APIs on behalf of a user
from google_auth_oauthlib.flow import InstalledAppFlow
# It's used to create a service object that lets your app interact with Google APIs like Calendar, Gmail, Drive, Sheets, etc.
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# A scope tells Google what level of access your app is requesting.
# Your app wants read and write access to all calendar features, including viewing, creating, editing, and deleting events
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # stores a previously authenticated token so users don’t need to log in again every time.
    token_path = "backend/agent/google_credentials/token.pickle"
    creds_path = "backend/agent/google_credentials/credentials.json"
    
    # This skips the need for launching a new browser OAuth flow if valid credentials already exist.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # creds is None OR creds exists but is invalid
    if not creds or not creds.valid:
        
        # creds exists, It’s expired, It has a refresh token (so it can get a new access token)
        if creds and creds.expired and creds.refresh_token:
            # Refreshes the credentials without asking the user to log in again
            creds.refresh(Request())
            
        else:
            # This loads your OAuth 2.0 credentials from the file credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=True)
            
        # creates the pickle file
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def block_calendar(time_string="9 AM"):
    service = get_calendar_service()

    # Extract time using regex (looks for patterns like "9 AM", "10 PM", etc.)
    match = re.search(r'(\d{1,2})\s*(AM|PM)', time_string, re.IGNORECASE)
    if not match:
        return "❌ Could not parse time. Please specify like '9 AM' or '3 PM'."

    hour = int(match.group(1))
    meridian = match.group(2).upper()

    if meridian == "PM" and hour != 12:
        hour += 12
    elif meridian == "AM" and hour == 12:
        hour = 0

    # Set time zone to IST
    local_tz = timezone("Asia/Kolkata")
    now = datetime.datetime.now(local_tz)
    start = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(hours=1)

    event = {
        'summary': 'Blocked by Agentic AI Assistant',
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"📅 Google Calendar event created for: {start.strftime('%I:%M %p IST')}"