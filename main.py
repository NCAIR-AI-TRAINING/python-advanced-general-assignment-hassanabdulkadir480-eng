from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    """Raised when the same visitor tries to check in consecutively."""
    pass

class EarlyEntryError(Exception):
    """Raised when any visitor tries to check in within 5 minutes of the last visitor."""
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create the file if it does not exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass  # create empty file

def get_last_visitor():
    """Return the last visitor's name and timestamp, or (None, None)."""
    if not os.path.exists(FILENAME):
        return None, None
    
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        if not lines:
            return None, None
        
        last_line = lines[-1].strip()
        name, timestamp = last_line.split(" | ")
        return name, datetime.fromisoformat(timestamp)

def add_visitor(visitor_name):
    """Add a visitor with duplicate and 5-minute early entry checks."""
    last_visitor, last_time = get_last_visitor()

    # Rule 1: No duplicate consecutive visitors
    if visitor_name == last_visitor:
        raise DuplicateVisitorError("Duplicate consecutive visitor not allowed.")

    # Rule 2: No visitor (anyone) within 5 minutes
    if last_time and (datetime.now() - last_time) < timedelta(minutes=5):
        raise EarlyEntryError("Must wait 5 minutes before next visitor.")

    # Log the visitor
    now = datetime.now().isoformat()
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {now}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
