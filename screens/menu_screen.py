"""
Menu Screen for Orion-DDH_v1 application
Displays the main menu with navigation options
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class MenuScreen(Screen):
    """Main menu screen with navigation options"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the menu UI"""
        # Use FloatLayout to allow background image
        root = FloatLayout()
        
        # Background image
        bg_image = Image(
            source='assets/background.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        root.add_widget(bg_image)
        
        # Semi-transparent overlay for better text readability
        overlay = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        with overlay.canvas.before:
            Color(0.1, 0.1, 0.15, 0.7)  # Semi-transparent dark overlay
            self.rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_rect, pos=self._update_rect)
        
        # App title
        title_label = Label(
            text='[b]Orion-DDH[/b]',
            markup=True,
            font_size=dp(28),
            size_hint_y=0.1,
            color=(0.9, 0.9, 0.95, 1)
        )
        overlay.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text='DDH Resistivity Data Logger',
            font_size=dp(14),
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.75, 1)
        )
        overlay.add_widget(subtitle_label)
        
        # Spacer where Doraemon used to be
        overlay.add_widget(Label(size_hint_y=0.35))
        
        # Menu buttons container
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=0.4
        )
        
        # Input New Data Button
        data_btn = Button(
            text='Input New Data',
            font_size=dp(18),
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        data_btn.bind(on_release=self.go_to_data_input)
        buttons_layout.add_widget(data_btn)
        
        # Hole ID Button
        holeid_btn = Button(
            text='Hole ID',
            font_size=dp(18),
            background_color=(0.3, 0.7, 0.5, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        holeid_btn.bind(on_release=self.go_to_holeid)
        buttons_layout.add_widget(holeid_btn)
        
        # Settings Button
        settings_btn = Button(
            text='Settings',
            font_size=dp(18),
            background_color=(0.5, 0.5, 0.55, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        settings_btn.bind(on_release=self.go_to_settings)
        buttons_layout.add_widget(settings_btn)
        
        overlay.add_widget(buttons_layout)
        
        # Spacer at bottom
        overlay.add_widget(Label(size_hint_y=0.1))
        
        # Version info
        version_label = Label(
            text='Version 1.3',
            font_size=dp(12),
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.55, 1)
        )
        overlay.add_widget(version_label)
        
        root.add_widget(overlay)
        self.add_widget(root)
    
    def _update_rect(self, instance, value):
        """Update background rectangle"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_to_data_input(self, instance):
        """Navigate to data input screen"""
        app = self.manager.get_screen('data_input')
        app.refresh_data()
        self.manager.transition.direction = 'left'
        self.manager.current = 'data_input'
    
    def go_to_holeid(self, instance):
        """Navigate to hole ID screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'holeid'
    
    def go_to_settings(self, instance):
        """Navigate to settings screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'settings'
