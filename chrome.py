import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class ChromeHistory:
    def __init__(self):
        self.history_file = self._get_history_path()
        
    def _get_history_path(self) -> str:
        """Get Chrome history file path based on OS"""
        home = str(Path.home())
        
        if os.name == 'nt':  # Windows
            return os.path.join(home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        elif os.name == 'posix':  # macOS/Linux
            if os.path.exists(os.path.join(home, 'Library')):  # macOS
                return os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome', 'Default', 'History')
            else:  # Linux
                return os.path.join(home, '.config', 'google-chrome', 'Default', 'History')
        
        raise Exception("Unsupported operating system")

    def get_history(self, days: int = 7) -> List[Dict]:
        """Get Chrome history for the last N days"""
        try:
            # Create a copy of history file since it might be locked
            temp_file = "temp_chrome_history"
            if os.path.exists(self.history_file):
                with open(self.history_file, 'rb') as f:
                    with open(temp_file, 'wb') as temp:
                        temp.write(f.read())

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Query the history
            conn = sqlite3.connect(temp_file)
            cursor = conn.cursor()
            
            query = """
                SELECT title, url, last_visit_time 
                FROM urls 
                WHERE last_visit_time > ? 
                ORDER BY last_visit_time DESC
            """
            
            # Convert datetime to Chrome timestamp format
            chrome_start_time = int((start_date - datetime(1601, 1, 1)).total_seconds() * 1000000)
            
            cursor.execute(query, (chrome_start_time,))
            results = cursor.fetchall()
            
            # Process results
            history = []
            for row in results:
                title, url, timestamp = row
                visit_time = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
                
                history.append({
                    'title': title,
                    'url': url,
                    'timestamp': visit_time.isoformat()
                })
            
            conn.close()
            os.remove(temp_file)
            
            return history
            
        except Exception as e:
            print(f"Error accessing Chrome history: {str(e)}")
            return []
