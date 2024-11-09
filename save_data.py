from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
import pandas as pd
from datetime import datetime
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from database import export_inventory_to_excel
class SaveScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Add instructions
        self.add_widget(Label(text="Choose a folder to save your file:"))

        # Add FileChooser configured for folder selection
        self.file_chooser = FileChooserIconView()
        self.file_chooser.dirselect = True  # Enable directory selection
        self.add_widget(self.file_chooser)
        
        layout=BoxLayout(orientation='horizontal',  # Arrange buttons in a row
                            size_hint=(1, None),      # Take full width, but fixed height
                            height=dp(60),            # Set height for the button layout
                            spacing=dp(10),           # Space between buttons
                            padding=dp(10)  )
        # Save button
        self.save_button = Button(text="Save", size_hint=(1, 0.1))
        self.save_button.bind(on_release=self.save_as_excel)
        
        
        self.back_button = Button(text="Back", size_hint=(1, 0.1))
        self.back_button.bind(on_release=self.back_action)
        layout.add_widget(self.save_button)
        layout.add_widget(self.back_button)
        
        self.add_widget(layout)
    
    def back_action(self,instance):
       
        self.parent.parent.current = 'home'
    def save_as_excel(self, instance):
        selected_folder = self.file_chooser.path  # Get the current selected folder
        if selected_folder:
            # Get the current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M")
            file_name = f"data {current_time}.xlsx"
            file_path = f"{selected_folder}/{file_name}"

            
        export_inventory_to_excel(file_path)  
        self.parent.parent.current = 'home'
class saving_data_screen(Screen):
    def __init__(self, **kwargs):
        super(saving_data_screen, self).__init__(**kwargs)
        self.saving_data_page = SaveScreen()  # Store reference to SearchPage
        self.add_widget(self.saving_data_page)

