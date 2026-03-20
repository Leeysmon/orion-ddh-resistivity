"""
Data Input Screen for Orion-DDH application
Excel-style data table for resistivity measurements
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.app import App
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from datetime import datetime
import os
import json


class OrionLogoWidget(Widget):
    """A widget displaying the Orion DDH logo"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0.1)
    
    def draw(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        scale = min(self.width, self.height) / 120
        
        with self.canvas:
            # Draw a stylized drill/geology icon
            # Drill tower (dark blue)
            Color(0.1, 0.3, 0.5, 1)
            # Tower legs
            Line(points=[cx - 20*scale, cy - 45*scale, cx - 10*scale, cy + 30*scale], width=3)
            Line(points=[cx + 20*scale, cy - 45*scale, cx + 10*scale, cy + 30*scale], width=3)
            # Cross beams
            Line(points=[cx - 15*scale, cy - 20*scale, cx + 15*scale, cy - 20*scale], width=2)
            Line(points=[cx - 12*scale, cy, cx + 12*scale, cy], width=2)
            Line(points=[cx - 8*scale, cy + 20*scale, cx + 8*scale, cy + 20*scale], width=2)
            
            # Drill rod (silver/gray)
            Color(0.6, 0.6, 0.7, 1)
            Line(points=[cx, cy + 30*scale, cx, cy - 50*scale], width=4)
            
            # Drill bit (gold/orange)
            Color(0.9, 0.6, 0.2, 1)
            Ellipse(pos=(cx - 6*scale, cy - 55*scale), size=(12*scale, 10*scale))
            
            # Rock layers at bottom
            Color(0.5, 0.4, 0.3, 1)
            Rectangle(pos=(cx - 35*scale, cy - 60*scale), size=(70*scale, 8*scale))
            Color(0.4, 0.5, 0.4, 1)
            Rectangle(pos=(cx - 35*scale, cy - 68*scale), size=(70*scale, 8*scale))
            Color(0.6, 0.5, 0.4, 1)
            Rectangle(pos=(cx - 35*scale, cy - 76*scale), size=(70*scale, 8*scale))


class DataInputScreen(Screen):
    """Screen for entering measurement data in a table format"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = []  # List of row data
        self.row_widgets = []  # List of row widget references
        self.row_layouts = []  # List of row layout widgets
        self.blank_count = 0  # Track consecutive blanks
        self.shown_blank_reminder = False  # Track if 4th blank popup shown
        self.zoom_scale = 1.0  # Default zoom scale
        self.headers_scroll = None  # Reference for synchronized scrolling
        self.table_scroll = None  # Reference for synchronized scrolling
        self._init_storage()
        self.build_ui()
    
    def _init_storage(self):
        """Initialize JSON storage for data persistence"""
        try:
            if platform == 'android':
                from android.storage import app_storage_path
                storage_path = app_storage_path()
            else:
                storage_path = '.'
            self.data_store = JsonStore(os.path.join(storage_path, 'input_data.json'))
        except Exception as e:
            print(f"Error initializing storage: {e}")
            self.data_store = None
    
    def _save_data(self):
        """Save current row data to persistent storage"""
        try:
            if self.data_store:
                # Convert rows to JSON-serializable format
                serializable_rows = []
                for row in self.rows:
                    row_copy = row.copy()
                    # Ensure all values are serializable
                    serializable_rows.append(row_copy)
                self.data_store.put('rows', data=serializable_rows)
                self.data_store.put('state', 
                    blank_count=self.blank_count,
                    shown_blank_reminder=self.shown_blank_reminder
                )
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def _load_data(self):
        """Load row data from persistent storage"""
        try:
            if self.data_store and self.data_store.exists('rows'):
                saved_rows = self.data_store.get('rows').get('data', [])
                if saved_rows:
                    # Clear existing rows first
                    self.rows = []
                    self.row_widgets = []
                    for layout in self.row_layouts:
                        self.table_layout.remove_widget(layout)
                    self.row_layouts = []
                    
                    # Restore saved rows
                    for row_data in saved_rows:
                        self._add_row_with_data(row_data)
                    
                    # Restore state
                    if self.data_store.exists('state'):
                        state = self.data_store.get('state')
                        self.blank_count = state.get('blank_count', 0)
                        self.shown_blank_reminder = state.get('shown_blank_reminder', False)
                    return True
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _add_row_with_data(self, row_data):
        """Add a row with pre-existing data"""
        row_index = len(self.rows)
        
        row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            size_hint_x=None,
            height=dp(60),
            spacing=dp(2)
        )
        row_layout.width = sum([w for _, w in self.column_headers]) + dp(2) * len(self.column_headers)
        
        row_widgets = {}
        
        # Create cells for each column
        for col_index, (col_name, col_width) in enumerate(self.column_headers):
            if col_name == 'Blank':
                # Checkbox for blank indicator
                checkbox_layout = BoxLayout(
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60)
                )
                with checkbox_layout.canvas.before:
                    Color(0.2, 0.2, 0.25, 1)
                    Rectangle(pos=checkbox_layout.pos, size=checkbox_layout.size)
                checkbox_layout.bind(pos=self._update_layout_bg, size=self._update_layout_bg)
                
                checkbox = CheckBox(
                    size_hint=(None, None),
                    size=(dp(40), dp(40)),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    active=row_data.get('is_blank', False)
                )
                checkbox.bind(active=lambda cb, val, ri=row_index: self.on_blank_checked(ri, val))
                checkbox_layout.add_widget(checkbox)
                row_widgets['blank_checkbox'] = checkbox
                row_layout.add_widget(checkbox_layout)
            elif col_name == 'Del':
                # Delete button
                del_btn = Button(
                    text='X',
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    background_color=(0.7, 0.2, 0.2, 1),
                    background_normal='',
                    font_size=dp(24)
                )
                del_btn.bind(on_release=lambda btn, ri=row_index: self.delete_row(ri))
                row_widgets['delete_btn'] = del_btn
                row_layout.add_widget(del_btn)
            elif col_name in ['Date', 'HoleID', 'Size', 'Time']:
                # Read-only auto-populated fields
                key_map = {'Date': 'date', 'HoleID': 'hole_id', 'Size': 'hole_size', 'Time': 'time'}
                field_key = key_map[col_name]
                
                cell = Label(
                    text=row_data.get(field_key, ''),
                    font_size=dp(18),
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    color=(0.7, 0.7, 0.75, 1),
                    halign='center',
                    valign='middle'
                )
                cell.bind(size=cell.setter('text_size'))
                
                with cell.canvas.before:
                    Color(0.2, 0.2, 0.25, 1)
                    Rectangle(pos=cell.pos, size=cell.size)
                
                row_widgets[field_key] = cell
                row_layout.add_widget(cell)
            elif col_name == 'Box #':
                # Box # field with numeric keyboard
                cell = TextInput(
                    text=row_data.get('box_num', ''),
                    multiline=False,
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    font_size=dp(20),
                    background_color=(0.22, 0.22, 0.27, 1),
                    foreground_color=(1, 1, 1, 1),
                    cursor_color=(1, 1, 1, 1),
                    padding=[dp(5), dp(15), dp(5), dp(15)],
                    halign='center',
                    input_filter='int',  # Numeric only
                    input_type='number'  # Numeric keyboard on mobile
                )
                cell.bind(text=lambda instance, value, ri=row_index: self.on_box_changed(ri, value, instance))
                row_widgets['box_num'] = cell
                row_layout.add_widget(cell)
            else:
                # Editable fields
                key_map = {'V1[V]': 'v1', 'V2[mV]': 'v2', 'Comment': 'comment'}
                field_key = key_map[col_name]
                
                cell = TextInput(
                    text=row_data.get(field_key, ''),
                    multiline=False,
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    font_size=dp(20),
                    background_color=(0.22, 0.22, 0.27, 1),
                    foreground_color=(1, 1, 1, 1),
                    cursor_color=(1, 1, 1, 1),
                    padding=[dp(5), dp(15), dp(5), dp(15)],
                    halign='center'
                )
                
                if field_key in ['v1', 'v2']:
                    cell.bind(text=lambda instance, value, ri=row_index, fn=field_key: self.on_numeric_changed(ri, fn, value))
                else:
                    cell.bind(text=lambda instance, value, ri=row_index, fn=field_key: self.on_field_changed(ri, fn, value))
                
                row_widgets[field_key] = cell
                row_layout.add_widget(cell)
        
        self.rows.append(row_data)
        self.row_widgets.append(row_widgets)
        self.row_layouts.append(row_layout)
        self.table_layout.add_widget(row_layout)
    
    def _update_layout_bg(self, instance, value):
        """Update layout background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.2, 0.25, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def build_ui(self):
        """Build the data input UI"""
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Background color
        with self.main_layout.canvas.before:
            Color(0.12, 0.12, 0.15, 1)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Header with back button and title
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text='< Menu',
            size_hint_x=0.2,
            background_color=(0.3, 0.3, 0.35, 1),
            background_normal='',
            font_size=dp(18)
        )
        back_btn.bind(on_release=self.go_back)
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]Data Input[/b]',
            markup=True,
            font_size=dp(24),
            size_hint_x=0.6,
            color=(0.9, 0.9, 0.95, 1)
        )
        header.add_widget(title)
        
        add_row_btn = Button(
            text='+ Row',
            size_hint_x=0.2,
            background_color=(0.3, 0.7, 0.5, 1),
            background_normal='',
            font_size=dp(18)
        )
        add_row_btn.bind(on_release=self.add_new_row)
        header.add_widget(add_row_btn)
        
        self.main_layout.add_widget(header)
        
        # Info bar showing current hole info
        self.info_bar = Label(
            text='Hole: Not Set | Size: Not Set',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(35),
            color=(0.6, 0.8, 0.6, 1)
        )
        self.main_layout.add_widget(self.info_bar)
        
        # Column headers (added Blank column before Box #)
        self.column_headers = [
            ('Date', dp(140)),
            ('HoleID', dp(120)),
            ('Size', dp(90)),
            ('Blank', dp(70)),    # New Blank checkbox column
            ('Box #', dp(100)),
            ('Time', dp(110)),
            ('V1[V]', dp(100)),
            ('V2[mV]', dp(110)),
            ('Comment', dp(140)),
            ('Del', dp(60)),  # Delete button column
        ]
        
        # Calculate total width
        total_width = sum([w for _, w in self.column_headers]) + dp(2) * len(self.column_headers)
        
        # Container for synchronized scrolling (headers + table together)
        scroll_container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        
        # Horizontal scroll wrapper - contains both headers and table
        self.h_scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=dp(10),
            bar_color=(0.5, 0.5, 0.6, 0.8),
            bar_inactive_color=(0.4, 0.4, 0.5, 0.5),
            scroll_type=['bars', 'content']
        )
        
        # Inner container - holds both header and table vertically
        inner_container = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            size_hint_y=1,
            width=total_width
        )
        
        # Headers layout (no separate scroll, part of inner container)
        headers_layout = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            size_hint_y=None,
            height=dp(50),
            spacing=dp(2),
            width=total_width
        )
        
        for col_name, col_width in self.column_headers:
            header_cell = Label(
                text=col_name,
                font_size=dp(20),
                size_hint=(None, None),
                width=col_width,
                height=dp(50),
                color=(0.9, 0.9, 0.95, 1),
                halign='center',
                valign='middle'
            )
            header_cell.bind(size=header_cell.setter('text_size'))
            
            # Add background
            with header_cell.canvas.before:
                Color(0.25, 0.35, 0.45, 1)
                Rectangle(pos=header_cell.pos, size=header_cell.size)
            header_cell.bind(pos=self._update_cell_bg, size=self._update_cell_bg)
            
            headers_layout.add_widget(header_cell)
        
        inner_container.add_widget(headers_layout)
        
        # Vertical scroll view for table data (inside the horizontal scroll)
        self.table_scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(12),
            bar_color=(0.4, 0.6, 0.8, 0.9),
            bar_inactive_color=(0.3, 0.4, 0.5, 0.6),
            scroll_type=['bars', 'content']
        )
        
        self.table_layout = GridLayout(
            cols=1,
            spacing=dp(2),
            size_hint_y=None,
            size_hint_x=None,
            width=total_width
        )
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        
        self.table_scroll.add_widget(self.table_layout)
        inner_container.add_widget(self.table_scroll)
        
        self.h_scroll.add_widget(inner_container)
        self.main_layout.add_widget(self.h_scroll)
        
        # Bottom action buttons
        bottom_buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(8),
            padding=[0, dp(5), 0, 0]
        )
        
        clear_btn = Button(
            text='Clear All',
            background_color=(0.6, 0.3, 0.3, 1),
            background_normal='',
            font_size=dp(18)
        )
        clear_btn.bind(on_release=self.clear_all_data)
        bottom_buttons.add_widget(clear_btn)
        
        export_btn = Button(
            text='Export CSV',
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal='',
            font_size=dp(18)
        )
        export_btn.bind(on_release=self.export_data)
        bottom_buttons.add_widget(export_btn)
        
        send_btn = Button(
            text='Send',
            background_color=(0.5, 0.3, 0.7, 1),
            background_normal='',
            font_size=dp(18)
        )
        send_btn.bind(on_release=self.send_data)
        bottom_buttons.add_widget(send_btn)
        
        self.main_layout.add_widget(bottom_buttons)
        
        self.add_widget(self.main_layout)
        
        # Add initial empty row
        Clock.schedule_once(lambda dt: self.add_new_row(None), 0.1)
    
    def _update_rect(self, instance, value):
        """Update background rectangle"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def _update_cell_bg(self, instance, value):
        """Update cell background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.25, 0.35, 0.45, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def refresh_data(self):
        """Refresh the display with current hole data"""
        app = App.get_running_app()
        hole_data = app.get_hole_data()
        
        if hole_data:
            self.info_bar.text = f"Hole: {hole_data.get('hole_id', 'Not Set')} | Size: {hole_data.get('hole_size', 'Not Set')}"
        else:
            self.info_bar.text = 'Hole: Not Set | Size: Not Set - Please set Hole ID first'
    
    def on_enter(self):
        """Called when screen is entered"""
        self.refresh_data()
        # Load saved data on first enter
        if len(self.rows) <= 1 and (not self.rows or not self.rows[0].get('box_num', '').strip()):
            loaded = self._load_data()
            if not loaded:
                # No saved data, ensure we have an empty row
                if len(self.rows) == 0:
                    self.add_new_row(None)
    
    def on_leave(self):
        """Called when screen is exited - automatically save data"""
        self._save_data()
    
    def go_back(self, instance):
        """Navigate back to menu, saving data first"""
        self._save_data()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def add_new_row(self, instance):
        """Add a new empty row to the table"""
        row_index = len(self.rows)
        
        row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            size_hint_x=None,
            height=dp(60),
            spacing=dp(2)
        )
        row_layout.width = sum([w for _, w in self.column_headers]) + dp(2) * len(self.column_headers)
        
        row_data = {
            'date': '',
            'hole_id': '',
            'hole_size': '',
            'is_blank': False,  # New field for blank checkbox
            'box_num': '',
            'time': '',
            'v1': '',
            'v2': '',
            'comment': '',
            'auto_filled': False
        }
        
        row_widgets = {}
        
        # Create cells for each column
        for col_index, (col_name, col_width) in enumerate(self.column_headers):
            if col_name == 'Blank':
                # Checkbox for blank indicator
                checkbox_layout = BoxLayout(
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60)
                )
                with checkbox_layout.canvas.before:
                    Color(0.2, 0.2, 0.25, 1)
                    Rectangle(pos=checkbox_layout.pos, size=checkbox_layout.size)
                checkbox_layout.bind(pos=self._update_layout_bg, size=self._update_layout_bg)
                
                checkbox = CheckBox(
                    size_hint=(None, None),
                    size=(dp(40), dp(40)),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                )
                checkbox.bind(active=lambda cb, val, ri=row_index: self.on_blank_checked(ri, val))
                checkbox_layout.add_widget(checkbox)
                row_widgets['blank_checkbox'] = checkbox
                row_layout.add_widget(checkbox_layout)
            elif col_name == 'Del':
                # Delete button
                del_btn = Button(
                    text='X',
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    background_color=(0.7, 0.2, 0.2, 1),
                    background_normal='',
                    font_size=dp(24)
                )
                del_btn.bind(on_release=lambda btn, ri=row_index: self.delete_row(ri))
                row_widgets['delete_btn'] = del_btn
                row_layout.add_widget(del_btn)
            elif col_name in ['Date', 'HoleID', 'Size', 'Time']:
                # Read-only auto-populated fields
                cell = Label(
                    text='',
                    font_size=dp(18),
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    color=(0.7, 0.7, 0.75, 1),
                    halign='center',
                    valign='middle'
                )
                cell.bind(size=cell.setter('text_size'))
                
                with cell.canvas.before:
                    Color(0.2, 0.2, 0.25, 1)
                    Rectangle(pos=cell.pos, size=cell.size)
                
                key_map = {'Date': 'date', 'HoleID': 'hole_id', 'Size': 'hole_size', 'Time': 'time'}
                row_widgets[key_map[col_name]] = cell
                row_layout.add_widget(cell)
            elif col_name == 'Box #':
                # Box # field with numeric keyboard only
                cell = TextInput(
                    text='',
                    multiline=False,
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    font_size=dp(20),
                    background_color=(0.22, 0.22, 0.27, 1),
                    foreground_color=(1, 1, 1, 1),
                    cursor_color=(1, 1, 1, 1),
                    padding=[dp(5), dp(15), dp(5), dp(15)],
                    halign='center',
                    input_filter='int',  # Numeric only
                    input_type='number'  # Show numeric keyboard on mobile
                )
                cell.bind(text=lambda instance, value, ri=row_index: self.on_box_changed(ri, value, instance))
                row_widgets['box_num'] = cell
                row_layout.add_widget(cell)
            else:
                # Editable fields (V1, V2, Comment)
                cell = TextInput(
                    text='',
                    multiline=False,
                    size_hint=(None, None),
                    width=col_width,
                    height=dp(60),
                    font_size=dp(20),
                    background_color=(0.22, 0.22, 0.27, 1),
                    foreground_color=(1, 1, 1, 1),
                    cursor_color=(1, 1, 1, 1),
                    padding=[dp(5), dp(15), dp(5), dp(15)],
                    halign='center'
                )
                
                key_map = {'V1[V]': 'v1', 'V2[mV]': 'v2', 'Comment': 'comment'}
                field_key = key_map[col_name]
                row_widgets[field_key] = cell
                
                if col_name in ['V1[V]', 'V2[mV]']:
                    cell.bind(text=lambda instance, value, ri=row_index, fn=field_key: self.on_numeric_changed(ri, fn, value))
                else:
                    cell.bind(text=lambda instance, value, ri=row_index, fn=field_key: self.on_field_changed(ri, fn, value))
                
                row_layout.add_widget(cell)
        
        self.rows.append(row_data)
        self.row_widgets.append(row_widgets)
        self.row_layouts.append(row_layout)
        self.table_layout.add_widget(row_layout)
        
        # Scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.table_scroll, 'scroll_y', 0), 0.1)
        
        # Save data after adding row
        self._save_data()
    
    def on_blank_checked(self, row_index, is_checked):
        """Handle Blank checkbox change"""
        if row_index >= len(self.rows):
            return
        
        self.rows[row_index]['is_blank'] = is_checked
        
        if is_checked:
            # Disable Box # field when Blank is checked
            if 'box_num' in self.row_widgets[row_index]:
                box_widget = self.row_widgets[row_index]['box_num']
                box_widget.text = ''
                box_widget.disabled = True
                box_widget.background_color = (0.15, 0.15, 0.18, 1)
            
            # Track blank entries
            self.blank_count += 1
            
            # Show 4th blank reminder
            if self.blank_count == 4 and not self.shown_blank_reminder:
                self.shown_blank_reminder = True
                Clock.schedule_once(lambda dt: self.show_blank_reminder(), 0.2)
            
            # Auto-fill date, time, hole_id, hole_size when blank is checked
            if not self.rows[row_index]['auto_filled']:
                self.auto_fill_row(row_index)
        else:
            # Re-enable Box # field
            if 'box_num' in self.row_widgets[row_index]:
                box_widget = self.row_widgets[row_index]['box_num']
                box_widget.disabled = False
                box_widget.background_color = (0.22, 0.22, 0.27, 1)
            
            if self.blank_count > 0:
                self.blank_count -= 1
        
        self._save_data()
    
    def delete_row(self, row_index):
        """Delete a specific row"""
        if row_index >= len(self.rows):
            return
        
        # Check if this was a blank row for tracking
        if self.rows[row_index].get('is_blank', False):
            self.blank_count = max(0, self.blank_count - 1)
        
        # Remove from table
        row_layout = self.row_layouts[row_index]
        self.table_layout.remove_widget(row_layout)
        
        # Remove from lists
        del self.rows[row_index]
        del self.row_widgets[row_index]
        del self.row_layouts[row_index]
        
        # Update row indices for delete buttons and checkboxes
        self._update_row_indices()
        
        # Ensure at least one row exists
        if len(self.rows) == 0:
            self.add_new_row(None)
        
        self._save_data()
    
    def _update_row_indices(self):
        """Update delete button and checkbox bindings after row deletion"""
        for i, widgets in enumerate(self.row_widgets):
            if 'delete_btn' in widgets:
                btn = widgets['delete_btn']
                btn.unbind(on_release=btn.on_release)
                btn.bind(on_release=lambda b, ri=i: self.delete_row(ri))
            if 'blank_checkbox' in widgets:
                cb = widgets['blank_checkbox']
                cb.unbind(active=cb.active)
                cb.bind(active=lambda checkbox, val, ri=i: self.on_blank_checked(ri, val))
    
    def on_box_changed(self, row_index, value, instance):
        """Handle Box # field change - trigger auto-fill"""
        if row_index >= len(self.rows):
            return
        
        self.rows[row_index]['box_num'] = value
        
        # Auto-fill date, time, hole_id, hole_size when box number is entered
        if value.strip() and not self.rows[row_index]['auto_filled']:
            self.auto_fill_row(row_index)
        
        self._save_data()
    
    def show_blank_reminder(self):
        """Show friendly reminder popup for 4th blank"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Orion logo widget
        logo = OrionLogoWidget(size_hint=(1, 0.5))
        content.add_widget(logo)
        
        # Message
        message = Label(
            text='Remember to take one more\nBlank measurement!\n\n(4th blank entry detected)',
            font_size=dp(16),
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        message.bind(size=message.setter('text_size'))
        content.add_widget(message)
        
        ok_btn = Button(
            text='OK',
            size_hint_y=None,
            height=dp(45),
            background_color=(0.2, 0.7, 0.9, 1),
            background_normal='',
            font_size=dp(16)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='🔔 ブランク測定リマインダー',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=True,
            separator_color=(0.2, 0.7, 0.9, 1)
        )
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def on_numeric_changed(self, row_index, field_name, value):
        """Handle numeric field changes"""
        if row_index < len(self.rows):
            self.rows[row_index][field_name] = value
            
            # Also trigger auto-fill if this is first numeric input
            if value.strip() and not self.rows[row_index]['auto_filled']:
                self.auto_fill_row(row_index)
    
    def on_field_changed(self, row_index, field_name, value):
        """Handle any field change"""
        if row_index < len(self.rows):
            self.rows[row_index][field_name] = value
            self._save_data()
    
    def auto_fill_row(self, row_index):
        """Auto-fill date, time, hole_id, and hole_size for a row"""
        if row_index >= len(self.rows):
            return
        
        app = App.get_running_app()
        hole_data = app.get_hole_data()
        
        now = datetime.now()
        
        # Update row data
        self.rows[row_index]['date'] = now.strftime('%Y-%m-%d')
        self.rows[row_index]['time'] = now.strftime('%H:%M:%S')
        self.rows[row_index]['hole_id'] = hole_data.get('hole_id', '') if hole_data else ''
        self.rows[row_index]['hole_size'] = hole_data.get('hole_size', '') if hole_data else ''
        self.rows[row_index]['auto_filled'] = True
        
        # Update widgets
        widgets = self.row_widgets[row_index]
        widgets['date'].text = self.rows[row_index]['date']
        widgets['time'].text = self.rows[row_index]['time']
        widgets['hole_id'].text = self.rows[row_index]['hole_id']
        widgets['hole_size'].text = self.rows[row_index]['hole_size']
        
        self._save_data()
    
    def clear_all_data(self, instance):
        """Clear all data after confirmation"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))
        
        # Warning message
        warning_label = Label(
            text='Continuing will delete all the entered data.\n\nAre you sure you want to continue?',
            font_size=dp(16),
            halign='center',
            valign='middle',
            color=(1, 0.8, 0.8, 1)
        )
        warning_label.bind(size=warning_label.setter('text_size'))
        content.add_widget(warning_label)
        
        buttons = BoxLayout(spacing=dp(15), size_hint_y=None, height=dp(50))
        
        cancel_btn = Button(
            text='Cancel',
            background_color=(0.4, 0.4, 0.45, 1),
            background_normal='',
            font_size=dp(16)
        )
        confirm_btn = Button(
            text='Yes, Clear All',
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal='',
            font_size=dp(16)
        )
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Confirm Clear All Data',
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=True
        )
        
        cancel_btn.bind(on_release=popup.dismiss)
        confirm_btn.bind(on_release=lambda x: self._do_clear(popup))
        
        popup.open()
    
    def _do_clear(self, popup):
        """Actually clear all data"""
        popup.dismiss()
        
        # Clear data
        self.rows = []
        self.row_widgets = []
        self.row_layouts = []
        self.table_layout.clear_widgets()
        self.blank_count = 0
        self.shown_blank_reminder = False
        
        # Clear persistent storage
        if self.data_store:
            try:
                if self.data_store.exists('rows'):
                    self.data_store.delete('rows')
                if self.data_store.exists('state'):
                    self.data_store.delete('state')
            except Exception as e:
                print(f"Error clearing storage: {e}")
        
        # Clear in data manager
        app = App.get_running_app()
        app.clear_measurements()
        
        # Add a fresh row
        self.add_new_row(None)
    
    def _generate_csv_file(self):
        """Generate CSV file and return filepath"""
        app = App.get_running_app()
        
        # Collect data from rows - include rows with box_num OR is_blank checked
        valid_rows = [row for row in self.rows if row.get('box_num', '').strip() or row.get('is_blank', False)]
        
        if not valid_rows:
            return None, 'No data to export. Enter some measurements first.'
        
        # Prepare rows for export, converting is_blank to 'Blank' in box_num
        export_rows = []
        for row in valid_rows:
            row_copy = row.copy()
            if row_copy.get('is_blank', False):
                row_copy['box_num'] = 'Blank'
            export_rows.append(row_copy)
        
        # Save measurements to data manager
        for row in export_rows:
            app.add_measurement(row.copy())
        
        # Get hole data
        hole_data = app.get_hole_data()
        hole_id = hole_data.get('hole_id', 'unknown') if hole_data else 'unknown'
        
        # Extract numeric box numbers (exclude "Blank" entries)
        box_numbers = []
        for row in export_rows:
            box_val = row.get('box_num', '').strip()
            if box_val.lower() != 'blank':
                try:
                    box_numbers.append(int(box_val))
                except ValueError:
                    pass  # Skip non-numeric box values
        
        # Determine box range for filename
        if box_numbers:
            min_box = min(box_numbers)
            max_box = max(box_numbers)
            box_range = f"Box {min_box} to {max_box}"
        else:
            box_range = "Box Data"
        
        # Generate filename: HoleID_Core Resistivity_Box XX to YY_YYYYMMDD.csv
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"{hole_id}_Core Resistivity_{box_range}_{date_str}.csv"
        
        # Determine filepath
        if platform == 'android':
            from android.storage import primary_external_storage_path
            filepath = f"{primary_external_storage_path()}/Download/{filename}"
        else:
            filepath = filename
        
        success = app.export_data(filepath)
        
        if success:
            return filepath, None
        else:
            return None, 'Could not export data. Check permissions.'
    
    def export_data(self, instance):
        """Export data to CSV"""
        filepath, error = self._generate_csv_file()
        
        if error:
            self.show_message('No Data' if 'No data' in error else 'Export Failed', error)
        else:
            self.show_message('Export Successful', f'Data exported to:\n{filepath}')
    
    def send_data(self, instance):
        """Send data via email - opens email app with CSV attached"""
        # Generate CSV file
        filepath, error = self._generate_csv_file()
        
        if error:
            self.show_message('No Data' if 'No data' in error else 'Error', error)
            return
        
        # Get settings for email
        try:
            settings_screen = self.manager.get_screen('settings')
            emails = settings_screen.get_registered_emails()
            logger_name = settings_screen.get_logger_name()
        except Exception:
            emails = []
            logger_name = ''
        
        # Get filename for subject
        import os
        filename = os.path.basename(filepath)
        # Remove .csv extension for cleaner subject
        subject = filename.replace('.csv', '') if filename.endswith('.csv') else filename
        
        # Create email body
        if logger_name:
            body = f"Hi,\n\nPlease find attached the updated drill core resistivity data.\n\nBest,\n{logger_name}"
        else:
            body = "Hi,\n\nPlease find attached the updated drill core resistivity data.\n\nBest regards"
        
        # Directly open email app with attachment
        try:
            if platform == 'android':
                self._send_android_email_direct(filepath, emails, subject, body)
            else:
                self._send_desktop_email_direct(filepath, emails, subject, body)
        except Exception as e:
            self.show_message('Send Failed', f'Could not open email app: {str(e)}')
    
    def _send_android_email_direct(self, filepath, emails, subject, body):
        """Open email app on Android with CSV attachment and pre-filled recipients"""
        try:
            from jnius import autoclass, cast
            from jnius import jarray
            
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            String = autoclass('java.lang.String')
            
            intent = Intent(Intent.ACTION_SEND)
            intent.setType('text/csv')  # CSV mime type
            
            # Add pre-registered email recipients
            if emails:
                java_email_array = jarray(String)(len(emails))
                for i, email in enumerate(emails):
                    java_email_array[i] = String(email)
                intent.putExtra(Intent.EXTRA_EMAIL, java_email_array)
            
            # Set subject to filename
            intent.putExtra(Intent.EXTRA_SUBJECT, String(subject))
            # Set email body with logger signature
            intent.putExtra(Intent.EXTRA_TEXT, String(body))
            
            # Attach file
            file = File(filepath)
            context = PythonActivity.mActivity.getApplicationContext()
            
            try:
                # Try to get FileProvider (for Android 7+)
                FileProvider = autoclass('androidx.core.content.FileProvider')
                authority = str(context.getPackageName()) + '.fileprovider'
                uri = FileProvider.getUriForFile(context, String(authority), file)
            except Exception:
                # Fallback to Uri.fromFile for older Android
                uri = Uri.fromFile(file)
            
            intent.putExtra(Intent.EXTRA_STREAM, cast('android.os.Parcelable', uri))
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            
            # Open email app chooser (Gmail will be an option)
            chooser = Intent.createChooser(intent, String('Send via Email'))
            PythonActivity.mActivity.startActivity(chooser)
            
        except Exception as e:
            self.show_message('Email Info', f'Data saved to:\n{filepath}\n\nPlease manually attach this file in your email app.')
    
    def _send_desktop_email_direct(self, filepath, emails, subject, body):
        """Open email client on desktop with file info"""
        try:
            import webbrowser
            import urllib.parse
            import os
            
            # Get just the filename for the message
            filename = os.path.basename(filepath)
            
            # URL encode subject and body
            encoded_subject = urllib.parse.quote(subject)
            full_body = f'{body}\n\nFile: {filename}\nLocation: {filepath}'
            encoded_body = urllib.parse.quote(full_body)
            
            # Build mailto with recipients if available
            recipients = ','.join(emails) if emails else ''
            mailto = f"mailto:{recipients}?subject={encoded_subject}&body={encoded_body}"
            
            webbrowser.open(mailto)
            self.show_message('Email Ready', f'Email client opened.\n\nPlease manually attach:\n{filepath}')
        except Exception as e:
            self.show_message('Email Info', f'Data saved to:\n{filepath}\n\nPlease email manually.')
    
    def _show_send_confirmation(self, filepath, emails):
        """Show confirmation popup before sending"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        recipient_text = '\n'.join(emails[:3])  # Show up to 3 emails
        content.add_widget(Label(
            text=f'Send data to:\n{recipient_text}',
            font_size=dp(12),
            halign='center'
        ))
        
        buttons = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(40))
        
        cancel_btn = Button(text='Cancel', background_color=(0.5, 0.5, 0.55, 1), background_normal='')
        send_btn = Button(text='Send', background_color=(0.5, 0.3, 0.7, 1), background_normal='')
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(send_btn)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Confirm Send',
            content=content,
            size_hint=(0.85, 0.45),
            auto_dismiss=True
        )
        
        cancel_btn.bind(on_release=popup.dismiss)
        send_btn.bind(on_release=lambda x: self._do_send(popup, filepath, emails))
        
        popup.open()
    
    def _do_send(self, popup, filepath, emails):
        """Actually send the email"""
        popup.dismiss()
        
        try:
            # For Android, we'll use an intent to send email
            if platform == 'android':
                self._send_android_email(filepath, emails)
            else:
                # For Windows testing, create a .eml file or show message
                self._send_desktop_email(filepath, emails)
        except Exception as e:
            self.show_message('Send Failed', f'Could not send email: {str(e)}')
    
    def _send_android_email(self, filepath, emails):
        """Send email on Android using intent"""
        try:
            from jnius import autoclass, cast
            from jnius import jarray
            
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            String = autoclass('java.lang.String')
            
            # Filter valid emails
            valid_emails = [email.strip() for email in emails if email.strip()]
            
            intent = Intent(Intent.ACTION_SEND)
            intent.setType('message/rfc822')  # Use rfc822 for better email app compatibility
            
            # Create proper Java String array for email recipients
            if valid_emails:
                # Create a Java String array using jarray
                java_email_array = jarray(String)(len(valid_emails))
                for i, email in enumerate(valid_emails):
                    java_email_array[i] = String(email)
                intent.putExtra(Intent.EXTRA_EMAIL, java_email_array)
            
            intent.putExtra(Intent.EXTRA_SUBJECT, String('Orion-DDH Resistivity Data'))
            intent.putExtra(Intent.EXTRA_TEXT, String('Please find attached the resistivity measurement data.'))
            
            # Attach file
            file = File(filepath)
            context = PythonActivity.mActivity.getApplicationContext()
            
            try:
                # Try to get FileProvider (for Android 7+)
                FileProvider = autoclass('androidx.core.content.FileProvider')
                authority = str(context.getPackageName()) + '.fileprovider'
                uri = FileProvider.getUriForFile(context, String(authority), file)
            except Exception:
                # Fallback to Uri.fromFile for older Android or if FileProvider not configured
                uri = Uri.fromFile(file)
            
            intent.putExtra(Intent.EXTRA_STREAM, cast('android.os.Parcelable', uri))
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            
            # Start email app chooser
            chooser = Intent.createChooser(intent, String('Send Email'))
            PythonActivity.mActivity.startActivity(chooser)
            
            self.show_message('Email', 'Opening email app...')
        except Exception as e:
            # If intent fails, show manual instructions
            self.show_message('Email Info', f'Data saved to:\n{filepath}\n\nTo send manually, open your email app and attach the file.\n\nRecipients:\n{", ".join(emails)}')
    
    def _send_desktop_email(self, filepath, emails):
        """Handle email on desktop (Windows) - open default mail client"""
        try:
            import webbrowser
            import urllib.parse
            
            subject = urllib.parse.quote('Orion-DDH Resistivity Data')
            body = urllib.parse.quote(f'Please find the data file at: {filepath}')
            mailto = f"mailto:{','.join(emails)}?subject={subject}&body={body}"
            
            webbrowser.open(mailto)
            self.show_message('Email', f'Opening email client...\n\nPlease manually attach:\n{filepath}')
        except Exception as e:
            self.show_message('Email Info', f'Data saved to:\n{filepath}\n\nPlease email manually to:\n{", ".join(emails)}')
    
    def show_message(self, title, message):
        """Show a message popup"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message, text_size=(dp(250), None), halign='center'))
        
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(40))
        content.add_widget(ok_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.45),
            auto_dismiss=True
        )
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()
