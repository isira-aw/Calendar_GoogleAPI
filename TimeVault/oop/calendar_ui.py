from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from calendar_api import authenticate_google_api, create_calendar_event  # Import the functions from your calendar API module

# Page 1: Signing Page
class SigningPage(Screen):
    pass

# Page 2: Books Page
class BooksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=[100, 10], spacing=10)
        self.fields = {}

        # Create a ScrollView to hold all the inputs and expand it to fill most of the screen
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=[10, 10])
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

        # Add input fields to the scroll layout
        input_fields = [
            "Summary", "Location", "Description", "Date (YYYY-MM-DD)",
            "Start Time (HH:MM:SS)", "End Time (HH:MM:SS)", "Time Zone", "Attendees (comma-separated emails)"
        ]

        for field in input_fields:
            text_input = TextInput(hint_text=field, multiline=False, size_hint_y=None, height=40)
            self.fields[field] = text_input
            self.scroll_layout.add_widget(text_input)

        # Attendees input field separately
        self.attendees_input = TextInput(hint_text='Attendees (comma-separated emails)', multiline=False, size_hint_y=None, height=40)
        self.scroll_layout.add_widget(self.attendees_input)

        # Add the scroll layout to the scroll view
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)

        # Add buttons for actions with size adjustment to fit the screen layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=[10, 0])

        create_event_button = Button(text='Create Event', size_hint=(0.33, 1))
        create_event_button.bind(on_press=self.create_event)
        button_layout.add_widget(create_event_button)

        reset_button = Button(text='Reset Fields', size_hint=(0.33, 1))
        reset_button.bind(on_press=self.reset_fields)
        button_layout.add_widget(reset_button)

        next_button = Button(text='Next', background_color=(0, 0, 1, 1), size_hint=(0.33, 1))
        next_button.bind(on_press=self.go_to_final_page)
        button_layout.add_widget(next_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

    def create_event(self, instance):
        try:
            # Authenticate Google API
            service = authenticate_google_api()

            date = self.fields["Date (YYYY-MM-DD)"].text
            start_time = self.fields["Start Time (HH:MM:SS)"].text
            end_time = self.fields["End Time (HH:MM:SS)"].text

            # Validate required fields
            if not all([date, start_time, end_time]):
                self.show_status("Please fill out all required fields.")
                return

            event_details = {
                "summary": self.fields["Summary"].text,
                "location": self.fields["Location"].text,
                "description": self.fields["Description"].text,
                "start_time": f"{date}T{start_time}+05:30",
                "end_time": f"{date}T{end_time}+05:30",
                "time_zone": self.fields["Time Zone"].text or "Asia/Colombo",
                "attendees": [
                    {"email": email.strip()} for email in self.attendees_input.text.split(',') if email.strip()
                ]
            }

            # Create calendar event using Google API
            created_event = create_calendar_event(service, event_details)
            self.show_status(f"Event created: {created_event.get('htmlLink')}")
        except Exception as ex:
            self.show_status(f"Error: {str(ex)}")

    def show_status(self, message):
        # Creating a label dynamically to display the status message
        status_label = Label(text=message, size_hint_y=None, height=40)
        self.scroll_layout.add_widget(status_label)

    def reset_fields(self, instance):
        # Reset the text in all fields
        for field in self.fields.values():
            field.text = ""
        self.attendees_input.text = ""

    def go_to_final_page(self, instance):
        self.manager.current = 'final_page'


# Page 3: Final Page
class FinalPage(Screen):
    def show_popup(self):
        # Create popup content
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.popup_input = TextInput(hint_text='Enter something', multiline=False, size_hint=(1, None), height=40)
        popup_layout.add_widget(self.popup_input)

        submit_button = Button(text='Submit')
        submit_button.bind(on_press=self.submit_input)
        popup_layout.add_widget(submit_button)

        # Create and open the popup
        self.popup = Popup(title='Popup Input', content=popup_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def submit_input(self, instance):
        # Update label text and close popup
        self.ids.result_label.text = self.popup_input.text
        self.popup.dismiss()


# Main App
class MyKivyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SigningPage(name='signing_page'))
        sm.add_widget(BooksPage(name='books_page'))
        sm.add_widget(FinalPage(name='final_page'))
        return sm


if __name__ == '__main__':
    MyKivyApp().run()
