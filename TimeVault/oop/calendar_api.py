import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Path to credentials.json
CREDENTIALS_FILE = r"D:\GitHUB\Calendar_GoogleAPI\TimeVault\backend\Credentials.json"

def authenticate_google_api():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"'{CREDENTIALS_FILE}' not found. Please ensure it is in the correct location."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def create_calendar_event(service, event_details):
    try:
        event = {
            "summary": event_details.get("summary"),
            "location": event_details.get("location"),
            "description": event_details.get("description"),
            "start": {
                "dateTime": event_details.get("start_time"),
                "timeZone": event_details.get("time_zone"),
            },
            "end": {
                "dateTime": event_details.get("end_time"),
                "timeZone": event_details.get("time_zone"),
            },
            "attendees": event_details.get("attendees"),
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return created_event

    except HttpError as error:
        raise Exception(f"An error occurred: {error}")
