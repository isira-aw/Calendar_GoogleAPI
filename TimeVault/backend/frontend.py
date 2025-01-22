from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

# Common button style for all buttons
def style_button(button, background_color, text_color=[1, 1, 1, 1]):
    button.background_normal = ''
    button.background_color = background_color
    button.color = text_color
    button.size_hint = (1, 0.1)
    button.height = 50
    return button

# Page 1: Signing Page
class SigningPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title_label = Label(text='Calendar', font_size=24, size_hint=(1, 0.2), halign='center')
        layout.add_widget(title_label)

        self.email_input = TextInput(hint_text='Enter your email', multiline=False, size_hint=(1, 0.1), height=40)
        layout.add_widget(self.email_input)

        enter_button = Button(text='Enter')
        style_button(enter_button, [0, 0, 1, 1])
        enter_button.bind(on_press=self.go_to_books_page)
        layout.add_widget(enter_button)

        self.add_widget(layout)

    def go_to_books_page(self, instance):
        self.manager.current = 'books_page'

# Page 2: Books Page
class BooksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        scroll_view = ScrollView(size_hint=(1, 0.6))
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        self.book_input = TextInput(hint_text='Enter book name', multiline=False, size_hint=(1, None), height=40)
        scroll_layout.add_widget(self.book_input)

        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)

        next_button = Button(text='Next')
        style_button(next_button, [0, 0, 1, 1])
        next_button.bind(on_press=self.go_to_final_page)
        layout.add_widget(next_button)

        back_button = Button(text='Back')
        style_button(back_button, [1, 1, 1, 1], text_color=[0, 0, 0, 1])
        back_button.bind(on_press=self.go_to_signing_page)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_final_page(self, instance):
        self.manager.current = 'final_page'

    def go_to_signing_page(self, instance):
        self.manager.current = 'signing_page'

# Page 3: Final Page
class FinalPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.final_button = Button(text='Click Me')
        style_button(self.final_button, [0, 0, 1, 1])
        self.final_button.size_hint = (0.5, 0.5)
        self.final_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.final_button.bind(on_press=self.show_popup)
        self.layout.add_widget(self.final_button)

        self.result_label = Label(size_hint=(1, 0.2))
        self.layout.add_widget(self.result_label)

        self.back_button = Button(text='Back')
        style_button(self.back_button, [1, 1, 1, 1], text_color=[0, 0, 0, 1])
        self.back_button.bind(on_press=self.go_to_books_page)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def show_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.popup_input = TextInput(hint_text='Enter something', multiline=False, size_hint=(1, None), height=40)
        popup_layout.add_widget(self.popup_input)

        submit_button = Button(text='Submit')
        style_button(submit_button, [0, 0, 1, 1])
        submit_button.bind(on_press=self.submit_input)
        popup_layout.add_widget(submit_button)

        self.popup = Popup(title='Popup Input', content=popup_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def submit_input(self, instance):
        self.result_label.text = self.popup_input.text
        self.popup.dismiss()
        self.update_layout_with_delete_button()

    def update_layout_with_delete_button(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.result_label)

        delete_button = Button(text='Delete')
        style_button(delete_button, [1, 0, 0, 1])
        delete_button.bind(on_press=self.delete_result)
        self.layout.add_widget(delete_button)

        self.layout.add_widget(self.final_button)
        self.layout.add_widget(self.back_button)

    def delete_result(self, instance):
        self.result_label.text = ''
        self.layout.clear_widgets()
        self.layout.add_widget(self.final_button)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.back_button)

    def go_to_books_page(self, instance):
        self.manager.current = 'books_page'

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
