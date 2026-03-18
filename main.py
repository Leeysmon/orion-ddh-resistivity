"""
Orion-DDH_v1 - Android Data Input Application
Main entry point for the Kivy application
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform

# Set window size for desktop testing (ignored on Android)
if platform != 'android':
    Window.size = (400, 700)

# Import screens
from screens.menu_screen import MenuScreen
from screens.holeid_screen import HoleIDScreen
from screens.data_input_screen import DataInputScreen
from screens.settings_screen import SettingsScreen

# Import data manager
from data.data_manager import DataManager


class OrionDDHApp(App):
    """Main application class for Orion-DDH_v1"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        self.title = "Orion-DDH_v1"
    
    def build(self):
        """Build the application UI"""
        # Create screen manager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(HoleIDScreen(name='holeid'))
        self.sm.add_widget(DataInputScreen(name='data_input'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        
        return self.sm
    
    def switch_screen(self, screen_name, direction='left'):
        """Switch to a different screen with animation"""
        self.sm.transition.direction = direction
        self.sm.current = screen_name
    
    def get_hole_data(self):
        """Get current hole data from data manager"""
        return self.data_manager.get_hole_data()
    
    def set_hole_data(self, hole_data):
        """Set hole data in data manager"""
        self.data_manager.set_hole_data(hole_data)
    
    def add_measurement(self, measurement):
        """Add a measurement to the data manager"""
        self.data_manager.add_measurement(measurement)
    
    def get_measurements(self):
        """Get all measurements from data manager"""
        return self.data_manager.get_measurements()
    
    def clear_measurements(self):
        """Clear all measurements"""
        self.data_manager.clear_measurements()
    
    def export_data(self, filepath):
        """Export data to CSV file"""
        return self.data_manager.export_to_csv(filepath)


if __name__ == '__main__':
    OrionDDHApp().run()
