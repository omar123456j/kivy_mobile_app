from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from database import *


class SearchPage(BoxLayout):
    
    filtered_clients = ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_list_article()
        self.filtered_clients = self.client_list
        
    def update_list_article(self):
        self.client_list=get_article_list()
        self.filtered_clients = self.client_list
        self.update_client_list_view()

    def filter_clients(self, search_text):
        """Filter clients based on 'Référence 1' and 'Désignation FR'."""
        search_text = search_text.lower()
        self.filtered_clients = [
            row for row in self.client_list if
            search_text in row['Référence 1'].lower() or search_text in row['Désignation FR'].lower()
        ]
        self.update_client_list_view()

    def update_client_list_view(self):
        """Update the RecycleView with the filtered clients."""
        client_data = [{'text': f"{row['Code']} | {row['Référence 1']} | {row['Désignation FR']} | {row['Unité/Colis']}"} for row in self.filtered_clients]
        self.ids.client_list_view.data = client_data
        

    def select_client(self, client_info):
        selected_code = client_info.split('|')[0].strip()
        selected_client = next((client for client in self.client_list if client['Code'] == selected_code), None)
        
        if selected_client:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            desc_label = Label(text=f"{selected_client['Code']} - {selected_client['Désignation FR']}", size_hint=(1, 0.2), font_size='18sp')
            colis_label = Label(text=f"There are {selected_client['Unité/Colis']} in each colisage.", size_hint=(1, 0.2))
            colis_label2=Label(text=f"{selected_client['Unité/Colis']}", size_hint=(1, 0.2))
            
            input_layout = GridLayout(cols=2, row_default_height=40, spacing=10)
            input_layout.add_widget(Label(text='Quantity Colisage:', size_hint_x=None, width=150))
            quantity_colis_input = TextInput(text='0', multiline=False)
            input_layout.add_widget(quantity_colis_input)

            input_layout.add_widget(Label(text='Quantity Par Pièce:', size_hint_x=None, width=150))
            quantity_piece_input = TextInput(text='0', multiline=False)
            input_layout.add_widget(quantity_piece_input)

            valid_button = Button(text="Valid", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
            valid_button.bind(on_release=lambda *args: self.show_confirmation_popup(selected_client, quantity_colis_input.text, quantity_piece_input.text,colis_label2.text))

            content.add_widget(desc_label)
            content.add_widget(colis_label)
            content.add_widget(input_layout)
            content.add_widget(valid_button)

            self.popup = Popup(title="Client Details", content=content, size_hint=(0.8, 0.5), auto_dismiss=True)
            self.popup.open()
    
    def show_confirmation_popup(self, selected_client, quantity_colis, quantity_piece,colis_unit):
                confirm_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
                message = Label(text="Do you confirm the validation?", size_hint=(1, 0.6))
                confirm_content.add_widget(message)
               
                buttons_layout = BoxLayout(size_hint=(1, 0.4), spacing=10)
                confirm_button = Button(text="Yes")
                cancel_button = Button(text="No")
                buttons_layout.add_widget(confirm_button)
                buttons_layout.add_widget(cancel_button)

                confirm_content.add_widget(buttons_layout)

                confirmation_popup = Popup(title="Confirmation", content=confirm_content, size_hint=(0.6, 0.3), auto_dismiss=True)

                # Bind the confirmation button to proceed with the validation
                confirm_button.bind(on_release=lambda *args: self.on_valid(selected_client, quantity_colis, quantity_piece,colis_unit))
                confirm_button.bind(on_release=confirmation_popup.dismiss)
                # Bind the cancel button to simply close the confirmation popup
                cancel_button.bind(on_release=confirmation_popup.dismiss)

                confirmation_popup.open()
    def on_valid(self, client, qty_colis, qty_piece,colis_unit):
        
        l=[(int(client['Code']), client['Référence 1'] , client['Désignation FR'] , float(qty_colis), float(qty_piece),float(colis_unit))]
        print(l)
        add_article(l)
        self.popup.dismiss()

class ClientSearch(Screen):
    def __init__(self, **kwargs):
        super(ClientSearch, self).__init__(**kwargs)
        self.search_page = SearchPage()  # Store reference to SearchPage
        self.add_widget(self.search_page)

    def update_articles(self):
        # Call the update function of the SearchPage
        self.search_page.update_list_article()

""" class ClientSearchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ClientSearch(name='test'))
        return sm

if __name__ == '__main__':
    ClientSearchApp().run() """
