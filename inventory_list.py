from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from database import get_inventory_list,update_inventory,delete_inventory_item
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp

class ClientButton1(BoxLayout):
    client_info = StringProperty()  # Property to hold client info

class ClientDataView(BoxLayout):
    filtered_clients = ListProperty([])
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.initial_list_inventory()
        #self.update_client_view()
         
    def update_client_view(self):
        
       
        client_data = [{'client_info': f"{row['id']} | {row['Référence 1']} | {row['Désignation FR']} | {row['colis']} |{row['unit']}", 'id': row['id']} for row in self.filtered_clients]
        client_data.reverse()
        # Assuming you are using RecycleView, set its data to client_data
        self.ids.client_list_view.data = client_data

    def edit_client(self, client_info):
        
       
        selected_code = client_info.split('|')[0].strip()
        
        print(client_info)
        
        selected_client = next((client for client in self.client_list if client['id'] == selected_code), None)
      
        if selected_client:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            input_layout=GridLayout(cols=2, row_default_height=15, spacing=10)
            input_3layout=GridLayout(cols=3, row_default_height=15, spacing=10)

            # Input fields for editing
            desc_label = Label(text=f"{selected_client['id']} - {selected_client['Référence 1']} -{selected_client['Désignation FR']}", size_hint=(1, 0.2), font_size='18sp')
            content.add_widget(desc_label)
            
            colis_label=Label(text=" number des coulis :")
            colis_input = TextInput(text=selected_client['colis'], hint_text='colis', multiline=True)
            input_layout.add_widget(colis_label)
            input_layout.add_widget(colis_input)
            
            unit_label=Label(text="number unit :")
            unit_input = TextInput(text=selected_client['unit'], hint_text='colis', multiline=True)
            input_layout.add_widget(unit_label)
            input_layout.add_widget(unit_input)
            
            
            button_layout = BoxLayout(
                            orientation='horizontal',  # Arrange buttons in a row
                            size_hint=(1, None),      # Take full width, but fixed height
                            height=dp(60),            # Set height for the button layout
                            spacing=dp(10),           # Space between buttons
                            padding=dp(10)            # Padding around the layout
                        )

            # Save Changes Button
            save_button = Button(
                text="Save Changes",
                size_hint=(None, None),
                size=(dp(100), dp(40)),
                background_color=(0.3, 0.7, 0.3, 1),  # Green background for Save
                color=(1, 1, 1, 1),  # White text
                bold=True,
            )
            save_button.bind(on_release=lambda *args: self.save_changes(selected_code, colis_input.text, unit_input.text))

            # Delete Button
            delete_button = Button(
                text="Delete",
                size_hint=(None, None),
                size=(dp(100), dp(40)),
                background_color=(0.9, 0.2, 0.2, 1),  # Red background for Delete
                color=(1, 1, 1, 1),
                bold=True,
            )
            delete_button.bind(on_release=lambda *args: self.delete_client(selected_code))

            # Cancel Button
            cancel_button = Button(
                text="Cancel",
                size_hint=(None, None),
                size=(dp(100), dp(40)),
                background_color=(0.8, 0.8, 0.8, 1),  # Gray background for Cancel
                color=(0, 0, 0, 1),  # Black text
                bold=True,
            )
            cancel_button.bind(on_release=lambda *args: self.Cancel_client())

            # Add buttons to the layout
            button_layout.add_widget(save_button)
            button_layout.add_widget(delete_button)
            button_layout.add_widget(cancel_button)

            # Finally, add the button_layout to your input_3layout
            input_3layout.add_widget(button_layout)
            
            content.add_widget(input_layout)
            content.add_widget(input_3layout)
            
            # Create and open the popup
            self.popup = Popup(title="Edit Client", content=content, size_hint=(0.8, 0.6))
            self.popup.open()

    def save_changes(self, id, colis,unit):
        print(f"id={id} annd colis={colis} and unit ={unit}")
        update_inventory(id,colis,unit)
        self.initial_list_inventory()
        self.popup.dismiss()
    def delete_client(self, id):
        print(id)
        delete_inventory_item(id)
        self.initial_list_inventory()
        self.popup.dismiss()
    def Cancel_client(self):self.popup.dismiss()   
    def initial_list_inventory(self):
        self.client_list=get_inventory_list()
        self.filtered_clients=self.client_list
        self.update_client_view()
        


class inventoryList(Screen):
    def __init__(self, **kwargs):
        super(inventoryList, self).__init__(**kwargs)
        self.inventory_page = ClientDataView()  # Store reference to SearchPage
        self.add_widget(self.inventory_page)
    def update_list(self):
        # Call the update function of the SearchPage
        self.inventory_page.initial_list_inventory()
    


""" class inventoryListApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(inventoryList(name='test'))
        return sm

if __name__ == '__main__':
    inventoryListApp().run()  """