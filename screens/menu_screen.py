"""
Menu Screen for Orion-DDH_v1 application
Displays the main menu with navigation options
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.clock import Clock


class DoraemonMenuWidget(Widget):
    """A fun Doraemon with Gambatte message for the menu"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0.1)
    
    def draw(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        scale = min(self.width, self.height) / 140
        
        with self.canvas:
            # Body (blue)
            Color(0.0, 0.6, 0.9, 1)
            Ellipse(pos=(cx - 40*scale, cy - 50*scale), size=(80*scale, 80*scale))
            
            # Face (white)
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - 34*scale, cy - 38*scale), size=(68*scale, 62*scale))
            
            # Eyes (white)
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - 20*scale, cy + 8*scale), size=(20*scale, 26*scale))
            Ellipse(pos=(cx, cy + 8*scale), size=(20*scale, 26*scale))
            
            # Pupils (black) - looking cheerful
            Color(0, 0, 0, 1)
            Ellipse(pos=(cx - 10*scale, cy + 15*scale), size=(10*scale, 14*scale))
            Ellipse(pos=(cx + 4*scale, cy + 15*scale), size=(10*scale, 14*scale))
            
            # Eye shine
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - 7*scale, cy + 22*scale), size=(4*scale, 5*scale))
            Ellipse(pos=(cx + 7*scale, cy + 22*scale), size=(4*scale, 5*scale))
            
            # Nose (red)
            Color(0.9, 0.2, 0.2, 1)
            Ellipse(pos=(cx - 7*scale, cy), size=(14*scale, 14*scale))
            
            # Nose line
            Color(0, 0, 0, 1)
            Line(points=[cx, cy, cx, cy - 28*scale], width=1.5)
            
            # Smile (big happy smile)
            Line(points=[cx - 28*scale, cy - 12*scale, cx - 15*scale, cy - 25*scale, 
                        cx, cy - 30*scale, cx + 15*scale, cy - 25*scale, 
                        cx + 28*scale, cy - 12*scale], width=2)
            
            # Whiskers
            Line(points=[cx - 40*scale, cy - 3*scale, cx - 20*scale, cy - 6*scale], width=1.2)
            Line(points=[cx - 40*scale, cy - 13*scale, cx - 20*scale, cy - 13*scale], width=1.2)
            Line(points=[cx - 40*scale, cy - 23*scale, cx - 20*scale, cy - 20*scale], width=1.2)
            Line(points=[cx + 40*scale, cy - 3*scale, cx + 20*scale, cy - 6*scale], width=1.2)
            Line(points=[cx + 40*scale, cy - 13*scale, cx + 20*scale, cy - 13*scale], width=1.2)
            Line(points=[cx + 40*scale, cy - 23*scale, cx + 20*scale, cy - 20*scale], width=1.2)
            
            # Collar (red)
            Color(0.9, 0.2, 0.2, 1)
            Ellipse(pos=(cx - 32*scale, cy - 55*scale), size=(64*scale, 14*scale))
            
            # Bell (yellow/gold)
            Color(1, 0.85, 0, 1)
            Ellipse(pos=(cx - 10*scale, cy - 60*scale), size=(20*scale, 20*scale))
            
            # Bell detail
            Color(0, 0, 0, 1)
            Line(points=[cx - 7*scale, cy - 50*scale, cx + 7*scale, cy - 50*scale], width=1.2)
            Line(points=[cx, cy - 50*scale, cx, cy - 42*scale], width=1.2)
            
            # Raised paw (waving)
            Color(0.0, 0.6, 0.9, 1)
            Ellipse(pos=(cx + 35*scale, cy + 10*scale), size=(22*scale, 22*scale))
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx + 38*scale, cy + 13*scale), size=(16*scale, 16*scale))


class MenuScreen(Screen):
    """Main menu screen with navigation options"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the menu UI"""
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Background color
        with layout.canvas.before:
            Color(0.15, 0.15, 0.2, 1)  # Dark blue-gray background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # App title
        title_label = Label(
            text='[b]Orion-DDH_v1[/b]',
            markup=True,
            font_size=dp(28),
            size_hint_y=0.1,
            color=(0.9, 0.9, 0.95, 1)
        )
        layout.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text='DDH Resistivity Data Logger',
            font_size=dp(14),
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.75, 1)
        )
        layout.add_widget(subtitle_label)
        
        # Doraemon with Gambatte message
        doraemon_container = BoxLayout(orientation='vertical', size_hint_y=0.35)
        
        doraemon = DoraemonMenuWidget(size_hint=(1, 0.8))
        doraemon_container.add_widget(doraemon)
        
        gambatte_label = Label(
            text='頑張って！(Gambatte!)',
            font_size=dp(18),
            size_hint_y=0.2,
            color=(1, 0.85, 0.2, 1)
        )
        doraemon_container.add_widget(gambatte_label)
        
        layout.add_widget(doraemon_container)
        
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
        
        layout.add_widget(buttons_layout)
        
        # Spacer at bottom
        layout.add_widget(Label(size_hint_y=0.1))
        
        # Version info
        version_label = Label(
            text='Version 1.0',
            font_size=dp(12),
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.55, 1)
        )
        layout.add_widget(version_label)
        
        self.add_widget(layout)
    
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
