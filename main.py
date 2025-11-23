from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            f.write("")

def get_last_visitor():
    ensure_file()
    with open(FILENAME, "r") as f:
        lines = f.readlines()
    if not lines:
        return None
    last_line = lines[-1].strip()
    try:
        name, timestamp = last_line.split(" | ")
        return name
    except:
        return None

def add_visitor(visitor_name):
    last_name = get_last_visitor()

    # Duplicate visitor rule
    if last_name == visitor_name:
        raise DuplicateVisitorError("Duplicate visitor not allowed")

    # Write visitor in required format
    timestamp = datetime.now().isoformat()
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {timestamp}\n")

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