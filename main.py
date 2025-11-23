from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
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
        return None, None

    last_line = lines[-1].strip()

    try:
        name, timestamp = last_line.split(" | ")
        return name, datetime.fromisoformat(timestamp)
    except:
        return None, None

def add_visitor(visitor_name):
    ensure_file()

    last_name, last_time = get_last_visitor()

    # RULE 1: Duplicate visitor rule (NO SAME NAME TWICE IN A ROW)
    if last_name == visitor_name:
        raise DuplicateVisitorError("This visitor just logged in")

    # RULE 2: 5-minute wait between DIFFERENT visitors
    if last_time is not None:
        minutes_passed = (datetime.now() - last_time).total_seconds() / 60
        if minutes_passed < 5:
            raise EarlyEntryError("Please wait 5 minutes before next visitor")

    # WRITE LOG ENTRY IN REQUIRED FORMAT
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