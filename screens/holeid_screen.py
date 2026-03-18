"""
Hole ID Screen for Orion-DDH_v1 application
Input screen for hole identification and metadata
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.app import App
from datetime import datetime


class HoleIDScreen(Screen):
    """Screen for entering hole identification data"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = {}
        self.build_ui()
    
    def build_ui(self):
        """Build the hole ID input UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Background color
        with main_layout.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Header with back button and title
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='< Back',
            size_hint_x=0.25,
            background_color=(0.3, 0.3, 0.35, 1),
            background_normal='',
            font_size=dp(14)
        )
        back_btn.bind(on_release=self.go_back)
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]Hole ID Setup[/b]',
            markup=True,
            font_size=dp(22),
            size_hint_x=0.75,
            color=(0.9, 0.9, 0.95, 1)
        )
        header.add_widget(title)
        
        main_layout.add_widget(header)
        
        # Scrollable form container
        scroll = ScrollView(size_hint=(1, 1))
        
        form_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Field definitions
        fields = [
            ('hole_id', 'Hole ID', 'e.g., DDH-001'),
            ('hole_size', 'Hole Size', 'e.g., NQ, HQ, PQ'),
            ('start_date', 'Start Date', 'YYYY-MM-DD'),
            ('end_date', 'End Date', 'YYYY-MM-DD'),
            ('project', 'Project', 'Project name'),
            ('logger', 'Logger', 'Logger name/ID'),
        ]
        
        for field_id, field_label, hint in fields:
            # Field container
            field_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(5)
            )
            
            # Label
            label = Label(
                text=field_label,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(25),
                halign='left',
                valign='middle',
                color=(0.8, 0.8, 0.85, 1)
            )
            label.bind(size=label.setter('text_size'))
            field_container.add_widget(label)
            
            # Input field
            text_input = TextInput(
                hint_text=hint,
                multiline=False,
                size_hint_y=None,
                height=dp(45),
                font_size=dp(16),
                background_color=(0.25, 0.25, 0.3, 1),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(1, 1, 1, 1),
                hint_text_color=(0.5, 0.5, 0.55, 1),
                padding=[dp(10), dp(10), dp(10), dp(10)]
            )
            
            # Set default date for date fields
            if field_id in ['start_date', 'end_date']:
                text_input.text = datetime.now().strftime('%Y-%m-%d')
            
            self.inputs[field_id] = text_input
            field_container.add_widget(text_input)
            
            form_layout.add_widget(field_container)
        
        # Add spacer
        spacer = BoxLayout(size_hint_y=None, height=dp(30))
        form_layout.add_widget(spacer)
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        # Bottom buttons
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(15)
        )
        
        # Clear button
        clear_btn = Button(
            text='Clear',
            background_color=(0.6, 0.3, 0.3, 1),
            background_normal='',
            font_size=dp(16)
        )
        clear_btn.bind(on_release=self.clear_fields)
        buttons_layout.add_widget(clear_btn)
        
        # Save button
        save_btn = Button(
            text='Save',
            background_color=(0.3, 0.7, 0.5, 1),
            background_normal='',
            font_size=dp(16)
        )
        save_btn.bind(on_release=self.save_data)
        buttons_layout.add_widget(save_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.add_widget(main_layout)
    
    def _update_rect(self, instance, value):
        """Update background rectangle"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        """Called when screen is entered - load existing data"""
        app = App.get_running_app()
        hole_data = app.get_hole_data()
        
        if hole_data:
            for field_id, value in hole_data.items():
                if field_id in self.inputs and value:
                    self.inputs[field_id].text = value
    
    def go_back(self, instance):
        """Navigate back to menu"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def clear_fields(self, instance):
        """Clear all input fields"""
        for field_id, text_input in self.inputs.items():
            if field_id in ['start_date', 'end_date']:
                text_input.text = datetime.now().strftime('%Y-%m-%d')
            else:
                text_input.text = ''
    
    def save_data(self, instance):
        """Save the hole ID data"""
        app = App.get_running_app()
        
        # Validate required fields
        if not self.inputs['hole_id'].text.strip():
            self.show_error('Hole ID is required')
            return
        
        if not self.inputs['hole_size'].text.strip():
            self.show_error('Hole Size is required')
            return
        
        # Collect data
        hole_data = {
            'hole_id': self.inputs['hole_id'].text.strip(),
            'hole_size': self.inputs['hole_size'].text.strip(),
            'start_date': self.inputs['start_date'].text.strip(),
            'end_date': self.inputs['end_date'].text.strip(),
            'project': self.inputs['project'].text.strip(),
            'logger': self.inputs['logger'].text.strip(),
        }
        
        # Save to data manager
        app.set_hole_data(hole_data)
        
        # Show confirmation
        self.show_confirmation('Hole ID data saved successfully!')
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
    
    def show_confirmation(self, message):
        """Show confirmation popup"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message))
        
        ok_btn = Button(
            text='OK',
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='Success',
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=True
        )
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()
