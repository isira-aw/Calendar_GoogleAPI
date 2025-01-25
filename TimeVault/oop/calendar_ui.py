from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from calendar_api import authenticate_google_api, create_calendar_event  # Import the functions from your calendar API module

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import Screen
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
from datetime import datetime
import os
from camera import CameraProcessor


# Page 1: Signing Page
class SigningPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Application title
        app_title = Label(
            text="TimeVault",
            font_size=48,
            bold=True,
            size_hint=(1, 0.3),
            halign="center",
            valign="middle",
            color=(0, 0, 1, 1),
        )
        app_title.bind(size=app_title.setter("text_size"))
        layout.add_widget(app_title)

        # User input for email
        self.email_input = TextInput(
            hint_text="Enter your email",
            multiline=False,
            size_hint=(1, 0.1),
            height=40,
        )
        layout.add_widget(self.email_input)

        # Submit button
        submit_button = Button(
            text="Submit",
            background_color=(0, 0, 1, 1),
            size_hint=(1, 0.1),
        )
        submit_button.bind(on_press=self.submit_email)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def submit_email(self, instance):
        """Handle email submission and navigate to the next page."""
        email = self.email_input.text.strip()
        if email:
            self.manager.current = "books_page"  # Navigate to the next page
        else:
            # Show an error message if email is not entered
            self.email_input.hint_text = "Please enter a valid email"
            self.email_input.focus = True
            
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


# # Page 3: Final Page
class FinalPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for the page
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Label to display extracted text
        self.extracted_text_label = Label(
            text="Extracted Text: None",
            size_hint=(1, None),
            height=250,
            color=(0, 1, 0, 1),
        )
        self.layout.add_widget(self.extracted_text_label)

        # Placeholder for the captured image
        self.captured_image = Image(size_hint=(1, None), height=300)
        self.layout.add_widget(self.captured_image)

        # Buttons container
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)

        # Add "Click Me" button to open the camera
        click_me_button = Button(text="Open Camera")
        click_me_button.bind(on_press=self.show_camera_popup)
        buttons_layout.add_widget(click_me_button)

        # Add "Back" button to navigate to the previous page
        back_button = Button(text="Back to Page 2")
        back_button.bind(on_press=self.go_back)
        buttons_layout.add_widget(back_button)

        self.layout.add_widget(buttons_layout)

        # Add the main layout to the screen
        self.add_widget(self.layout)

        # File path for the captured image
        self.saved_image_path = None

    def show_camera_popup(self, instance):
        """Show a pop-up with the camera interface."""
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Add Camera widget
        self.camera = Camera(resolution=(640, 480), play=True)
        popup_layout.add_widget(self.camera)

        # Buttons container for the popup
        popup_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        # Capture button
        capture_button = Button(text="Capture")
        capture_button.bind(on_press=self.capture_image)
        popup_buttons_layout.add_widget(capture_button)

        # Back button for the popup
        popup_back_button = Button(text="Back")
        popup_back_button.bind(on_press=self.close_popup)
        popup_buttons_layout.add_widget(popup_back_button)

        popup_layout.add_widget(popup_buttons_layout)

        # Create and open the popup
        self.popup = Popup(title="Camera", content=popup_layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def capture_image(self, instance):
        """Capture an image from the camera and extract text."""
        if self.camera.texture:
            # Get the texture from the camera
            texture = self.camera.texture
            size = texture.size
            buffer = texture.pixels

            # Save the texture as an image
            pil_image = PILImage.frombytes("RGBA", size, buffer)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"captured_image_{timestamp}.png"
            self.saved_image_path = os.path.join(os.getcwd(), file_name)
            pil_image.save(self.saved_image_path)

            # Load the image into the Kivy Image widget
            self.captured_image.texture = Texture.create(size=size, colorfmt="rgba")
            self.captured_image.texture.blit_buffer(buffer, colorfmt="rgba", bufferfmt="ubyte")
            self.captured_image.texture.flip_vertical()

            # Stop the camera and close the popup
            self.camera.play = False
            self.popup.dismiss()

            # Extract text from the captured image
            extracted_text = CameraProcessor.extract_text(self.saved_image_path)

            # Update the extracted text label
            self.extracted_text_label.text = f"Extracted Text: {extracted_text}"

    def close_popup(self, instance):
        """Stop the camera and close the popup."""
        if self.camera.play:
            self.camera.play = False
        self.popup.dismiss()

    def go_back(self, instance):
        """Navigate back to the previous page (Page 2)."""
        self.manager.current = "books_page"
        self.camera.play = False


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
