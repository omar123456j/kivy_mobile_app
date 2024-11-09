
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from plyer import filechooser
import pandas as pd
import sqlite3
import os
from database import *
from search import ClientSearch
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView 
from save_data import saving_data_screen
from login import login_screen,LoginScreen
Builder.load_file('inventorylist.kv')  
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.metrics import dp

class Home_page(Screen):
    def __init__(self, **kwargs):
        super(Home_page, self).__init__(**kwargs)
        
        # Create the main layout (vertical box) with spacing and padding for better mobile fit
        layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 20], spacing=20)

        # Add the logo image at the top (with size_hint for mobile screen adjustment)
        logo = Image(source='images/logo.png', size_hint=(1, 0.3), allow_stretch=True, keep_ratio=True)
        layout.add_widget(logo)

        # Create buttons with mobile-friendly size_hint and pos_hint
        button1 = Button(text='Importer la liste des articles', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5})
        button2 = Button(text='Inventaire de stock', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5})
        button3 = Button(text="List d'inventaire", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5})
        button4 = Button(text='Export as Excel', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5})
        button5 = Button(
            text='Clear DataBase (X)', 
            size_hint=(None, None),
            pos_hint={'center_x': 0.5},
            size=(dp(200), dp(70)),
            background_color=(1, 0, 0, 1),  # Red background for Clear
            color=(1, 1, 1, 1),  # White text
            bold=True,
        )

        # Set up button actions
        button1.bind(on_press=self.import_database)
        button2.bind(on_press=self.on_click_stock_inventory_window)
        button3.bind(on_press=self.on_click_list_inventory)
        button4.bind(on_press=self.open_filechooser)
        button5.bind(on_press=self.on_click_clear_DB)

        # Add buttons to the layout (center-aligned)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)
        self.add_widget(layout)
        
    def on_click_clear_DB(self, instance):
        # Create a BoxLayout for the Popup content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a label for the confirmation message
        content.add_widget(Label(text="Are you sure you want to clear the database?"))

        # Confirm button
        confirm_button = Button(text="Yes", size_hint_y=None, height=50)
        confirm_button.bind(on_release=lambda x: self.confirm_clear_db())

        # Cancel button
        cancel_button = Button(text="No", size_hint_y=None, height=50)
        cancel_button.bind(on_release=lambda x: self.popup.dismiss())

        # Add buttons to the layout
        content.add_widget(confirm_button)
        content.add_widget(cancel_button)

        # Create the Popup
        self.popup = Popup(title="Confirm Clear Database", content=content, size_hint=(0.8, 0.4))

        # Open the Popup
        self.popup.open()

    def confirm_clear_db(self):
        clear_db()
        self.popup.dismiss()

    def open_filechooser(self, instance):
            self.manager.current="saving_data_screen"

    def export_data_base(self, filechooser):
        try:
            # Accessing the selection from the passed filechooser instance
            selected = filechooser.selection
            print(f"Selected folder: {selected}")  # Debugging output

            if selected:
                folder_path = selected[0]
                file_path = f"{folder_path}/inventory.xlsx"  # Define the file name to save
                print(f"Exporting to: {file_path}")  # Confirm which file is being exported to
                export_inventory_to_excel(file_path)  # Save to the selected file path
            else:
                print("No folder selected.")  # Debugging output for empty selection

            self.popup_export.dismiss()
        except:print("error")
    def on_click_stock_inventory_window(self, instance):
        self.manager.current = 'clientsearch'
        client_search_screen = self.manager.get_screen('clientsearch')
        client_search_screen.update_articles()

    def on_click_list_inventory(self, instance):
        self.manager.current = 'test'
        client_search_screen = self.manager.get_screen('test')
        client_search_screen.update_list()

    def import_database(self, instance):
        filechooser.open_file(on_selection=self.on_file_selection)

    def on_file_selection(self, selection):
        if selection:
            excel_file = selection[0]
            try:
               import_excel_to_db(excel_file)
            except:print("errore")

""" class ClientSearchApp(App):
    def build(self):
        
        app_directory = self.user_data_dir  # Kivy automatically sets this for Android
        self.db_path = os.path.join(app_directory, 'articles.db')
        set_db_path(self.db_path)
        
        
        sm = ScreenManager()
        sm.add_widget(login_screen(name="login"))
        sm.add_widget(Home_page(name='home'))
        
        
        sm.add_widget(ClientSearch(name='clientsearch'))  # Add the ClientSearch screen
        from inventory_list import inventoryList
        sm.add_widget(inventoryList(name='test'))
        sm.add_widget(saving_data_screen(name="saving_data_screen"))
        return sm """

class ClientSearchApp(App):
    def build(self):
      try:
        app_directory = self.user_data_dir
        self.db_path = os.path.join(app_directory, 'articles.db')
        set_db_path(self.db_path)
        
        # Initialize the ScreenManager
        sm = ScreenManager()
        sm.add_widget(login_screen(name="login"))
        sm.add_widget(Home_page(name='home'))
        sm.add_widget(ClientSearch(name='clientsearch'))
        from inventory_list import inventoryList
        sm.add_widget(inventoryList(name='test'))
        sm.add_widget(saving_data_screen(name="saving_data_screen"))

        cl = sm.get_screen('login')
        cl.set_screen_manager(sm)
        cl.set_validity()
        return sm
      except Exception as e:
            # If there's an error during the initialization, show it in a popup
            self.show_error_popup(str(e))
        
        

    def show_error_popup(self, error_message):
        # Create a Popup to show the error message
        popup = Popup(
            title="Error",
            content=Label(text=error_message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

# Run the app
if __name__ == '__main__':
    ClientSearchApp().run()
