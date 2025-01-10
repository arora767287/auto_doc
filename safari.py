import os
import plistlib
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

class SafariHistory:
    def __init__(self):
        self.history_file = self._get_history_path()
        
    def _get_history_path(self) -> str:
        """Get Safari history file path"""
        home = str(Path.home())
        
        if os.name == 'posix' and os.path.exists(os.path.join(home, 'Library')):  # macOS
            return os.path.join(home, 'Library', 'Safari', 'History.db')
        
        raise Exception("Safari history is only available on macOS")

    def get_history(self, days: int = 7) -> List[Dict]:
        """Get Safari history for the last N days"""
        try:
            if not os.path.exists(self.history_file):
                return []
                
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Use sqlite3 to read Safari's History.db
            import sqlite3
            conn = sqlite3.connect(self.history_file)
            cursor = conn.cursor()
            
            query = """
                SELECT title, url, visit_time 
                FROM history_items 
                JOIN history_visits ON history_items.id = history_visits.history_item 
                WHERE visit_time > ? 
                ORDER BY visit_time DESC
            """
            
            # Convert datetime to Safari timestamp format
            safari_start_time = start_date.timestamp()
            
            cursor.execute(query, (safari_start_time,))
            results = cursor.fetchall()
            
            # Process results
            history = []
            for row in results:
                title, url, timestamp = row
                visit_time = datetime.fromtimestamp(timestamp)
                
                history.append({
                    'title': title,
                    'url': url,
                    'timestamp': visit_time.isoformat()
                })
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"Error accessing Safari history: {str(e)}")
            return []
