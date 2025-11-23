from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
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
            return None, None
        last_line = lines[-1]
        try:
            timestamp_str, visitor_name = last_line.split(" | ", 1)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return visitor_name, timestamp
        except ValueError:
            return None, None

def add_visitor(visitor_name):
    last_visitor, last_time = get_last_visitor()
    now = datetime.now()

    if last_visitor == visitor_name:
        raise DuplicateVisitorError("This visitor just logged in. Wait for someone else first.")

    if last_time and now - last_time < timedelta(minutes=5):
        raise EarlyEntryError("Please wait 5 minutes between different visitors.")

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
    except EarlyEntryError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)

if __name__ == "__main__":
    main()
