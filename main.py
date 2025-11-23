from datetime import datetime
import os

# Exception for duplicate visitor
class DuplicateVisitorError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            f.write("")

def get_last_visitor():
    ensure_file()
    with open(FILENAME, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return None
        last_line = lines[-1]
        try:
            _, visitor_name = last_line.split(" | ", 1)
            return visitor_name
        except ValueError:
            return None

def add_visitor(visitor_name):
    last_visitor = get_last_visitor()

    # Rule: No duplicate consecutive visitors
    if last_visitor == visitor_name:
        raise DuplicateVisitorError("Duplicate visitor")

    # Append visitor to file
    now = datetime.now()
    with open(FILENAME, 'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {visitor_name}\n")