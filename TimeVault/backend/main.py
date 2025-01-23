import os
import datetime as dt

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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

class CalendarEventApp(App):
    def build(self):
        button_style = {
            'size_hint': (0.5, 1),
            'background_normal': '',
            'background_color': (0.2, 0.6, 0.8, 1),
        }

        self.service = authenticate_google_api()

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.fields = {}
        labels = ["Summary", "Location", "Description", "Date (YYYY-MM-DD)", "Start Time (HH:MM:SS)",
                  "End Time (HH:MM:SS)", "Time Zone"]
        for label in labels:
            self.layout.add_widget(Label(text=label))
            self.fields[label] = TextInput(multiline=False)
            self.layout.add_widget(self.fields[label])

        self.layout.add_widget(Label(text="Attendees (comma-separated emails)"))
        self.attendees_input = TextInput(multiline=False)
        self.layout.add_widget(self.attendees_input)

        button_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        self.submit_button = Button(text="Create Event", **button_style)
        self.submit_button.bind(on_press=self.create_event)
        button_row.add_widget(self.submit_button)

        self.reset_button = Button(text="Reset Fields", **button_style)
        self.reset_button.bind(on_press=self.reset_fields)
        button_row.add_widget(self.reset_button)

        self.layout.add_widget(button_row)

        self.status_label = Label(text="", size_hint=(1, 0.2))
        self.layout.add_widget(self.status_label)

        return self.layout

    def create_event(self, instance):
        try:
            date = self.fields["Date (YYYY-MM-DD)"].text
            start_time = self.fields["Start Time (HH:MM:SS)"].text
            end_time = self.fields["End Time (HH:MM:SS)"].text

            # Validate required fields
            if not all([date, start_time, end_time]):
                self.status_label.text = "Please fill out all required fields."
                return

            event = {
                "summary": self.fields["Summary"].text,
                "location": self.fields["Location"].text,
                "description": self.fields["Description"].text,
                "start": {
                    "dateTime": f"{date}T{start_time}+00:00",
                    "timeZone": self.fields["Time Zone"].text or "UTC",
                },
                "end": {
                    "dateTime": f"{date}T{end_time}+00:00",
                    "timeZone": self.fields["Time Zone"].text or "UTC",
                },
                "attendees": [
                    {"email": email.strip()} for email in self.attendees_input.text.split(',') if email.strip()
                ]
            }

            created_event = self.service.events().insert(calendarId="primary", body=event).execute()
            self.status_label.text = f"Event created: {created_event.get('htmlLink')}"

        except HttpError as error:
            self.status_label.text = f"An error occurred: {error}"
        except Exception as ex:
            self.status_label.text = f"Error: {str(ex)}"

    def reset_fields(self, instance):
        for field in self.fields.values():
            field.text = ""
        self.attendees_input.text = ""
        self.status_label.text = ""

if __name__ == "__main__":
    CalendarEventApp().run()


