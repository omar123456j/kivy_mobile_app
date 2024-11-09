from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import platform
from fire_base import send_data
from functions import get_device_serial_A,is_password_valid
from database import update_user,get_user_data
from kivy.uix.screenmanager import ScreenManager, Screen
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None  # Store the ScreenManager reference
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Title label
        self.add_widget(Label(text="Login Page", font_size=24, size_hint_y=None, height=40))

        # Email input
        self.email = TextInput(hint_text="Enter your email", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.email)

        # Password input
        self.password = TextInput(hint_text="Enter your password", password=True, multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.password)

        # Submit button
        submit_button = Button(text="Submit", size_hint_y=None, height=40)
        submit_button.bind(on_release=self.submit)
        self.add_widget(submit_button)

        # Request a code button
        request_code_button = Button(text="Request a Code", size_hint_y=None, height=40)
        request_code_button.bind(on_release=self.request_code)
        self.add_widget(request_code_button)

        # Check if the device and user data are valid at initialization
      

    def check_validity(self):
        """Check user data validity on initialization."""
        user_data = get_user_data()
        device_serial = get_device_serial_A()
        check = is_password_valid(device_serial, user_data)
        print(check)
        if check:
            print("Valid credentials, redirecting to home window")
            self.screen_manager.current = 'home'  # Switch to the home screen
        else:
            print("Invalid credentials")

    def submit(self, instance):
        """Handle login submission and validate user credentials."""
        device_serial = get_device_serial_A()
        result = is_password_valid(device_serial, self.password.text)
        
        if result:
            update_user("admin", self.password.text)
            print("Valid credentials, redirecting to home window")
            self.screen_manager.current = 'home'  # Switch to the home screen
        else:
            print("Invalid credentials")

    def request_code(self, instance):
        """Request a new code by sending data to the server."""
        if not self.email.text:
            return
        send_data(self.email.text, get_device_serial_A())
        print("Code sent")
      
class login_screen(Screen):
    def __init__(self, **kwargs):
        super(login_screen, self).__init__(**kwargs)
        self.login = LoginScreen()  # Store reference to SearchPage
        self.add_widget(self.login)
    def set_screen_manager(self,SM):
        self.login.screen_manager=SM
    def set_validity(self):
        self.login.check_validity()