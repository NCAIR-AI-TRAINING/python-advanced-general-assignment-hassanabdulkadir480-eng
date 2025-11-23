from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create the file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            f.write("")  # create empty file

def get_last_visitor():
    """Return the last visitor name and their timestamp, or None if no visitors yet."""
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        return None, None
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None, None
        last_line = lines[-1].strip()
        try:
            timestamp_str, visitor_name = last_line.split(" | ")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return visitor_name, timestamp
        except ValueError:
            return None, None

def add_visitor(visitor_name):
    """Add a visitor to the log enforcing rules."""
    last_visitor, last_time = get_last_visitor()
    
    now = datetime.now()
    
    # Rule 1: No duplicate consecutive visitors
    if last_visitor == visitor_name:
        raise DuplicateVisitorError("This visitor just logged in. Wait for someone else first.")
    
    # Rule 2: 5-minute wait between different visitors
    if last_time and now - last_time < timedelta(minutes=5):
        raise EarlyEntryError("Please wait 5 minutes between different visitors.")
    
    # Append visitor to file
    with open(FILENAME, 'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {visitor_name}\n")
