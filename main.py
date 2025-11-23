from datetime import datetime, timedelta
import os

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
        name, timestamp_str = last_line.split(" | ")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return name, timestamp
    except:
        return None, None

def add_visitor(name):
    last_name, last_time = get_last_visitor()
    now = datetime.now()

    # Rule 1: duplicate visitor
    if last_name == name:
        raise Exception("Duplicate")

    # Rule 2: enforce 5 minute wait
    if last_time and (now - last_time).total_seconds() < 300:
        raise Exception("Wait")

    # Write correct format: Name | timestamp
    with open(FILENAME, "a") as f:
        f.write(f"{name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
