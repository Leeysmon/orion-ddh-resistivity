"""
Settings Screen for Orion-DDH application
Application settings and configuration
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform


class SettingsScreen(Screen):
    """Screen for application settings"""
    
    # Default emails
    DEFAULT_EMAILS = [
        'Leeymon-Hulijeli@irvresources.com',
        '',
        ''
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = {}
        self.email_inputs = []
        self.build_ui()
        self.load_settings()
    
    def get_storage_path(self):
        """Get the appropriate storage path for settings"""
        if platform == 'android':
            from android.storage import app_storage_path
            return f"{app_storage_path()}/settings.json"
        else:
            return 'settings.json'
    
    def build_ui(self):
        """Build the settings UI"""
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
            text='[b]Settings[/b]',
            markup=True,
            font_size=dp(22),
            size_hint_x=0.75,
            color=(0.9, 0.9, 0.95, 1)
        )
        header.add_widget(title)
        
        main_layout.add_widget(header)
        
        # Scrollable settings with visible scroll bars
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(12),
            bar_color=(0.4, 0.6, 0.8, 0.9),
            bar_inactive_color=(0.3, 0.4, 0.5, 0.6),
            scroll_type=['bars', 'content']
        )
        
        settings_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))
        
        # ===== REGISTER EMAIL ADDRESSES SECTION =====
        email_section_label = Label(
            text='[b]Register Email Addresses[/b]',
            markup=True,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            color=(0.9, 0.9, 0.95, 1)
        )
        email_section_label.bind(size=email_section_label.setter('text_size'))
        settings_layout.add_widget(email_section_label)
        
        # Create 3 email input fields
        for i in range(3):
            email_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(70),
                spacing=dp(3)
            )
            email_label = Label(
                text=f'Email {i + 1}' + (' (Primary)' if i == 0 else ''),
                font_size=dp(14),
                size_hint_y=None,
                height=dp(20),
                halign='left',
                valign='middle',
                color=(0.7, 0.7, 0.75, 1)
            )
            email_label.bind(size=email_label.setter('text_size'))
            email_container.add_widget(email_label)
            
            email_input = TextInput(
                hint_text='Enter email address',
                text=self.DEFAULT_EMAILS[i],
                multiline=False,
                size_hint_y=None,
                height=dp(40),
                font_size=dp(14),
                background_color=(0.25, 0.25, 0.3, 1),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(1, 1, 1, 1),
                hint_text_color=(0.5, 0.5, 0.55, 1),
                padding=[dp(10), dp(10), dp(10), dp(10)]
            )
            self.email_inputs.append(email_input)
            email_container.add_widget(email_input)
            settings_layout.add_widget(email_container)
        
        # Separator
        separator = BoxLayout(size_hint_y=None, height=dp(15))
        settings_layout.add_widget(separator)
        
        # Auto-save toggle
        autosave_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50)
        )
        autosave_label = Label(
            text='Auto-save data',
            font_size=dp(16),
            halign='left',
            color=(0.8, 0.8, 0.85, 1)
        )
        autosave_label.bind(size=autosave_label.setter('text_size'))
        autosave_container.add_widget(autosave_label)
        
        self.autosave_switch = Switch(active=True, size_hint_x=0.3)
        autosave_container.add_widget(self.autosave_switch)
        settings_layout.add_widget(autosave_container)
        
        # Zoom/Magnification slider
        zoom_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            spacing=dp(5)
        )
        
        zoom_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
        zoom_label = Label(
            text='Display Zoom',
            font_size=dp(16),
            halign='left',
            color=(0.8, 0.8, 0.85, 1)
        )
        zoom_label.bind(size=zoom_label.setter('text_size'))
        zoom_header.add_widget(zoom_label)
        
        self.zoom_value_label = Label(
            text='100%',
            font_size=dp(16),
            size_hint_x=0.3,
            halign='right',
            color=(0.3, 0.8, 0.5, 1)
        )
        self.zoom_value_label.bind(size=self.zoom_value_label.setter('text_size'))
        zoom_header.add_widget(self.zoom_value_label)
        zoom_container.add_widget(zoom_header)
        
        self.zoom_slider = Slider(
            min=50,
            max=200,
            value=100,
            step=10,
            size_hint_y=None,
            height=dp(50)
        )
        self.zoom_slider.bind(value=self.on_zoom_change)
        zoom_container.add_widget(self.zoom_slider)
        settings_layout.add_widget(zoom_container)
        
        # Default Logger Name
        logger_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5)
        )
        logger_label = Label(
            text='Default Logger Name',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle',
            color=(0.8, 0.8, 0.85, 1)
        )
        logger_label.bind(size=logger_label.setter('text_size'))
        logger_container.add_widget(logger_label)
        
        self.logger_input = TextInput(
            hint_text='Enter default logger name',
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
        logger_container.add_widget(self.logger_input)
        settings_layout.add_widget(logger_container)
        
        # Default Project Name
        project_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5)
        )
        project_label = Label(
            text='Default Project Name',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle',
            color=(0.8, 0.8, 0.85, 1)
        )
        project_label.bind(size=project_label.setter('text_size'))
        project_container.add_widget(project_label)
        
        self.project_input = TextInput(
            hint_text='Enter default project name',
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
        project_container.add_widget(self.project_input)
        settings_layout.add_widget(project_container)
        
        # Export format info
        format_info = Label(
            text='Export Format: CSV\nLocation: Downloads folder (Android)',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(60),
            halign='left',
            valign='top',
            color=(0.6, 0.6, 0.65, 1)
        )
        format_info.bind(size=format_info.setter('text_size'))
        settings_layout.add_widget(format_info)
        
        # Spacer
        spacer = BoxLayout(size_hint_y=None, height=dp(30))
        settings_layout.add_widget(spacer)
        
        # About section
        about_label = Label(
            text='[b]About[/b]',
            markup=True,
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            color=(0.9, 0.9, 0.95, 1)
        )
        about_label.bind(size=about_label.setter('text_size'))
        settings_layout.add_widget(about_label)
        
        about_info = Label(
            text='Orion-DDH\nDDH Resistivity Data Logger\nVersion 2.2\n\nFor geological resistivity\nmeasurement data collection.',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(120),
            halign='left',
            valign='top',
            color=(0.7, 0.7, 0.75, 1)
        )
        about_info.bind(size=about_info.setter('text_size'))
        settings_layout.add_widget(about_info)
        
        scroll.add_widget(settings_layout)
        main_layout.add_widget(scroll)
        
        # Bottom buttons
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(15)
        )
        
        reset_btn = Button(
            text='Reset Defaults',
            background_color=(0.6, 0.3, 0.3, 1),
            background_normal='',
            font_size=dp(16)
        )
        reset_btn.bind(on_release=self.reset_defaults)
        buttons_layout.add_widget(reset_btn)
        
        save_btn = Button(
            text='Save Settings',
            background_color=(0.3, 0.7, 0.5, 1),
            background_normal='',
            font_size=dp(16)
        )
        save_btn.bind(on_release=self.save_settings)
        buttons_layout.add_widget(save_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.add_widget(main_layout)
    
    def _update_rect(self, instance, value):
        """Update background rectangle"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_back(self, instance):
        """Navigate back to menu"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def load_settings(self):
        """Load settings from storage"""
        try:
            store = JsonStore(self.get_storage_path())
            if store.exists('settings'):
                self.settings = store.get('settings')
                self.autosave_switch.active = self.settings.get('autosave', True)
                self.logger_input.text = self.settings.get('default_logger', '')
                self.project_input.text = self.settings.get('default_project', '')
                
                # Load zoom
                zoom = self.settings.get('zoom', 100)
                self.zoom_slider.value = zoom
                self.zoom_value_label.text = f'{int(zoom)}%'
                
                # Load emails
                emails = self.settings.get('emails', self.DEFAULT_EMAILS)
                for i, email_input in enumerate(self.email_inputs):
                    if i < len(emails):
                        email_input.text = emails[i]
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self, instance=None):
        """Save settings to storage"""
        try:
            # Collect emails
            emails = [inp.text.strip() for inp in self.email_inputs]
            
            self.settings = {
                'autosave': self.autosave_switch.active,
                'default_logger': self.logger_input.text,
                'default_project': self.project_input.text,
                'emails': emails,
                'zoom': self.zoom_slider.value
            }
            
            store = JsonStore(self.get_storage_path())
            store.put('settings', **self.settings)
            
            self.show_message('Settings Saved', 'Your settings have been saved.')
        except Exception as e:
            print(f"Error saving settings: {e}")
            self.show_message('Error', f'Could not save settings: {e}')
    
    def reset_defaults(self, instance):
        """Reset to default settings"""
        self.autosave_switch.active = True
        self.logger_input.text = ''
        self.project_input.text = ''
        self.zoom_slider.value = 100
        
        # Reset emails to defaults
        for i, email_input in enumerate(self.email_inputs):
            email_input.text = self.DEFAULT_EMAILS[i]
        
        self.show_message('Reset', 'Settings reset to defaults.')
    
    def on_zoom_change(self, instance, value):
        """Handle zoom slider change"""
        self.zoom_value_label.text = f'{int(value)}%'
    
    def get_zoom_scale(self):
        """Get the current zoom scale factor (1.0 = 100%)"""
        return self.zoom_slider.value / 100.0
    
    def get_registered_emails(self):
        """Get list of non-empty registered emails"""
        return [inp.text.strip() for inp in self.email_inputs if inp.text.strip()]
    
    def get_logger_name(self):
        """Get the registered logger name"""
        return self.logger_input.text.strip() if self.logger_input.text else ''
    
    def show_message(self, title, message):
        """Show a message popup"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message))
        
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(40))
        content.add_widget(ok_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=True
        )
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()
