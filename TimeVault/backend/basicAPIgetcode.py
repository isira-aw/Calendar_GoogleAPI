
import os
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = r"...Calendar_GoogleAPI\TimeVault\backend\Credentials.json"

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

   
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

      
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
       
        service = build('calendar', 'v3', credentials=creds)

        # Event details
        event = {
            'summary': 'My Python Event',
            'location': 'Somewhere Online',
            'description': 'Some more details on this awesome event',
            'colorId': '5',
            'start': {
                'dateTime': '2025-01-23T09:00:00+02:00',
                'timeZone': 'Europe/Vienna'
            },
            'end': {
                'dateTime': '2025-01-23T17:00:00+02:00',
                'timeZone': 'Europe/Vienna'
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'social@neuralnine.com'},
                {'email': 'someemailthathopefullydoesnotexist@mail.com'}
            ]
        }
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
