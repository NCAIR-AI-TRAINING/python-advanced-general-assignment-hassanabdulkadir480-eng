from datetime import datetime
import os

# Custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create the file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            f.write("")  # empty file

def get_last_visitor():
    """Return the last visitor name, or None if no visitors yet."""
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
    """Add a visitor, enforcing duplicate visitor rule."""
    last_visitor = get_last_visitor()

    # Rule: No duplicate consecutive visitors
    if last_visitor == visitor_name:
        raise DuplicateVisitorError("This visitor just logged in. Wait for someone else first.")

    # Append visitor to the file
    now = datetime.now()
    with open(FILENAME, 'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {visitor_name}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ").strip()
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except DuplicateVisitorError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
