"""
Data Manager for Orion-DDH application
Handles data storage, retrieval, and export
"""

import csv
import json
import os
from datetime import datetime
from kivy.utils import platform


class DataManager:
    """
    Manages all data operations for the Orion-DDH application.
    Handles hole data, measurements, and CSV export.
    """
    
    def __init__(self):
        """Initialize the data manager"""
        self.hole_data = None
        self.measurements = []
        self._load_persisted_data()
    
    def get_storage_path(self):
        """Get the appropriate storage path"""
        if platform == 'android':
            from android.storage import app_storage_path
            return app_storage_path()
        else:
            return '.'
    
    def _load_persisted_data(self):
        """Load persisted data from storage"""
        try:
            data_file = os.path.join(self.get_storage_path(), 'orion_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.hole_data = data.get('hole_data')
                    self.measurements = data.get('measurements', [])
        except Exception as e:
            print(f"Error loading persisted data: {e}")
    
    def _save_persisted_data(self):
        """Save data to persistent storage"""
        try:
            data_file = os.path.join(self.get_storage_path(), 'orion_data.json')
            data = {
                'hole_data': self.hole_data,
                'measurements': self.measurements
            }
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving persisted data: {e}")
    
    def get_hole_data(self):
        """Get the current hole data dictionary"""
        return self.hole_data
    
    def set_hole_data(self, hole_data):
        """
        Set the hole data.
        
        Args:
            hole_data (dict): Dictionary containing hole information
                - hole_id: Hole identifier
                - hole_size: Hole size category (NQ, HQ, PQ, etc.)
                - start_date: Start date of drilling
                - end_date: End date of drilling
                - project: Project name
                - logger: Logger name/ID
        """
        self.hole_data = hole_data
        self._save_persisted_data()
    
    def add_measurement(self, measurement):
        """
        Add a measurement record.
        
        Args:
            measurement (dict): Dictionary containing measurement data
                - date: Date of measurement
                - hole_id: Hole identifier
                - hole_size: Hole size
                - box_num: Box number
                - time: Time of measurement
                - v1: V1 voltage reading
                - v2: V2 millivolt reading
                - comment: Additional comments
        """
        # Avoid duplicates based on date, time, and box_num
        for existing in self.measurements:
            if (existing.get('date') == measurement.get('date') and
                existing.get('time') == measurement.get('time') and
                existing.get('box_num') == measurement.get('box_num')):
                # Update existing measurement
                existing.update(measurement)
                self._save_persisted_data()
                return
        
        self.measurements.append(measurement)
        self._save_persisted_data()
    
    def get_measurements(self):
        """Get all measurement records"""
        return self.measurements
    
    def clear_measurements(self):
        """Clear all measurement records"""
        self.measurements = []
        self._save_persisted_data()
    
    def export_to_csv(self, filepath):
        """
        Export all data to a CSV file.
        
        Args:
            filepath (str): Path to the output CSV file
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                # Write header info
                csvfile.write(f"# Orion-DDH Data Export\n")
                csvfile.write(f"# Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                # Write hole info if available
                if self.hole_data:
                    csvfile.write(f"# Hole ID: {self.hole_data.get('hole_id', '')}\n")
                    csvfile.write(f"# Hole Size: {self.hole_data.get('hole_size', '')}\n")
                    csvfile.write(f"# Project: {self.hole_data.get('project', '')}\n")
                    csvfile.write(f"# Logger: {self.hole_data.get('logger', '')}\n")
                    csvfile.write(f"# Start Date: {self.hole_data.get('start_date', '')}\n")
                    csvfile.write(f"# End Date: {self.hole_data.get('end_date', '')}\n")
                
                csvfile.write("#\n")
                
                # Write measurement data
                if self.measurements:
                    headers = ['Date', 'HoleID', 'HoleSize', 'Blank', 'Box #', 'Time', 'V1[V]', 'V2[mV]', 'Comment']
                    writer = csv.DictWriter(
                        csvfile,
                        fieldnames=['date', 'hole_id', 'hole_size', 'is_blank', 'box_num', 'time', 'v1', 'v2', 'comment'],
                        extrasaction='ignore'
                    )
                    
                    # Write custom header
                    csvfile.write(','.join(headers) + '\n')
                    
                    # Write data rows
                    for measurement in self.measurements:
                        row = {
                            'date': measurement.get('date', ''),
                            'hole_id': measurement.get('hole_id', ''),
                            'hole_size': measurement.get('hole_size', ''),
                            'is_blank': 'Yes' if measurement.get('is_blank', False) else '',
                            'box_num': measurement.get('box_num', ''),
                            'time': measurement.get('time', ''),
                            'v1': measurement.get('v1', ''),
                            'v2': measurement.get('v2', ''),
                            'comment': measurement.get('comment', '')
                        }
                        writer.writerow(row)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def get_summary(self):
        """
        Get a summary of current data.
        
        Returns:
            dict: Summary information
        """
        return {
            'hole_id': self.hole_data.get('hole_id') if self.hole_data else None,
            'measurement_count': len(self.measurements),
            'has_data': len(self.measurements) > 0
        }
